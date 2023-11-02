#!/usr/bin/env python3

from subprocess import run
from json import loads, load
from json.decoder import JSONDecodeError
from pathlib import Path

import os


def check_for_rebase():
    # initialize variables
    default_image_ref = []
    current_image_ref = []
    default_image_tag = ""
    image_tag = ""

    try:
        with open("/usr/share/ublue-os/image-info.json") as f:
            image_info = load(f)
            default_image_ref = image_info["image-ref"].split(":")
            default_image_tag = image_info["image-tag"]
    except (FileNotFoundError, KeyError):
        print("uBlue image info file does not exist")
        return False, ""

    # Branch away from the default tag when one is set
    branch_file = Path("/etc/ublue-update/branch")
    if branch_file.exists():
        with branch_file.open() as f:
            branch = f.readline()
            branch_file.unlink()
            if branch:
                return (
                    True,
                    f"{default_image_ref[0]}:{default_image_ref[1]}:{default_image_ref[2]}:{branch}",
                )

    status_cmd = [
        "rpm-ostree",
        "status",
        "--pending-exit-77",
        "-b",
        "--json",
    ]
    status_out = run(status_cmd, capture_output=True)
    if status_out.returncode != 0:
        print(status_out.stdout.decode("utf-8"))
        return False, ""

    try:
        current_image_ref = (
            loads(status_out.stdout)["deployments"][0]["container-image-reference"]
            .replace(
                "ostree-unverified-registry:", "ostree-unverified-image:docker://"
            )  # replace shorthand
            .split(":")
        )
         # if the same ref as image-info.json then skip rebase
        if current_image_ref[:-1] == default_image_ref:
            return False, ""
    except (JSONDecodeError, KeyError, IndexError):
        print("unable to parse JSON output")
        print(status_out.stdout.decode("utf-8"))
        return False, ""

    image_tag = default_image_tag
    try:
        # if we are on an offline ISO installation
        # rebase to image-info.json defaults
        if current_image_ref[2] == "/var/ublue-os/image":
            return (
                True,
                f"{default_image_ref[0]}:{default_image_ref[1]}:{default_image_ref[2]}:{default_image_tag}",
            )

        # if current installation doesn't match image-info.json
        # skip rebase to be safe
        if current_image_ref[2] != default_image_ref[2]:
            return False, ""

        # We want to rebase so preserve image tag when rebasing unsigned
        if current_image_ref[2] == default_image_ref[2]:
            image_tag = current_image_ref[3]
    except IndexError:
        print("unable to get image tag from current deployment!")

    return (
        True,
        f"{default_image_ref[0]}:{default_image_ref[1]}:{default_image_ref[2]}:{image_tag}",
    )


if __name__ == "__main__":
    rpm_ostree = os.access("/usr/bin/rpm-ostree", os.X_OK)
    if not rpm_ostree:
        print("system isn't managed by rpm-ostree")
        os._exit(1)
    rebase, image_ref = check_for_rebase()
    if rebase:
        rebase_cmd = ["rpm-ostree", "rebase", image_ref]
        print(image_ref)
        rebase_out = run(rebase_cmd, capture_output=True)
        if rebase_out.returncode == 0:
            os._exit(0)  # rebase sucessful
        else:
            print("rebase failed!, command output:")
            print(rebase_out.stdout.decode("utf-8"))
    update_cmd = ["rpm-ostree", "upgrade"]
    update_out = run(update_cmd, capture_output=True)
    if update_out.returncode != 0:
        print(
            f"rpm-ostree upgrade returned code {update_out.returncode}, program output:"
        )
        print(update_out.stdout.decode("utf-8"))
        os._exit(update_out.returncode)

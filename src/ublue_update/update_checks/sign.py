from json import loads
from os import mknod
from re import match
from subprocess import run, PIPE


def get_image_ref():
    """Pull image identifiers"""
    with open("/etc/default/image-info", "r") as image_info:
        image_identifiers = {}
        for identifier in image_info:
            val, key = identifier.split("=")
            image_identifiers[val] = str(key).rstrip()

    """Set image identifiers"""
    image_name = image_identifiers.get("IMAGE_NAME")
    image_vendor = image_identifiers.get("IMAGE_VENDOR")
    fedora_version = image_identifiers.get("FEDORA_MAJOR_VERSION")

    """Construct image reference"""
    image = "ghcr.io/" + image_vendor + "/" + image_name + ":" + fedora_version
    return image


def rebase_image(image):
    """Regex in case vendor isn't ublue-os"""
    if match("/var/.+/image", image):
        image = get_image_ref()

    """Set protocol if unset"""
    protocol = "docker://"
    if protocol not in image:
        image = protocol + image

    """Rebase to signed image"""
    image = "ostree-image-signed:" + image
    rpm_ostree_rebase = ["rpm-ostree", "rebase", image]
    rebase = run(rpm_ostree_rebase, stdout=PIPE)
    if rebase.returncode == 0:
        mknod("/etc/ublue-update/image-signed")


def sign_image():
    """Pull ostree status"""
    rpm_ostree_status = ["rpm-ostree", "status", "--json"]
    status = run(rpm_ostree_status, stdout=PIPE).stdout

    """Parse current image"""
    deployments = loads(status)["deployments"][0]
    image_ref = deployments["container-image-reference"].split(":", 1)
    image = image_ref[1]

    """Rebase"""
    rebase_image(image)

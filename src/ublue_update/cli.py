import os
import subprocess
import logging
import argparse
import pwd
import psutil

from ublue_update.update_checks.system import system_update_check
from ublue_update.update_checks.wait import transaction_wait
from ublue_update.update_inhibitors.hardware import check_hardware_inhibitors
from ublue_update.config import load_value


def get_xdg_runtime_dir(uid):
    return f"/run/{pwd.getpwuid(uid).pw_name}/{uid}"


def notify(title: str, body: str, actions: list = [], urgency: str = "normal"):
    if not dbus_notify:
        return
    process_uid = os.getuid()
    args = [
        "/usr/bin/notify-send",
        title,
        body,
        "--app-name=Universal Blue Updater",
        "--icon=software-update-available-symbolic",
        f"--urgency={urgency}",
    ]
    if process_uid == 0:
        users = psutil.users()
        for user in users:
            xdg_runtime_dir = get_xdg_runtime_dir(pwd.getpwnam(user.name).pw_uid)
            user_args = [
                "sudo",
                "-u",
                f"{user.name}",
                "DISPLAY=:0",
                f"DBUS_SESSION_BUS_ADDRESS=unix:path={xdg_runtime_dir}/bus",
            ]
            print(user_args)
            user_args += args
            out = subprocess.run(
                user_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
        return
    if actions != []:
        for action in actions:
            args.append(f"--action={action}")
    out = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return out


def ask_for_updates():
    if not dbus_notify:
        return
    out = notify(
        "System Updater",
        "Update available, but system checks failed. Update now?",
        ["universal-blue-update-confirm=Confirm"],
        "critical",
    )
    # if the user has confirmed
    if "universal-blue-update-confirm" in out.stdout.decode("utf-8"):
        run_updates(cli_args)


def check_for_updates(checks_failed: bool) -> bool:
    """Tracks whether any updates are available"""
    update_available: bool = False
    system_update_available: bool = system_update_check()
    if system_update_available:
        update_available = True
    if update_available:
        return True
    log.info("No updates are available.")
    return False


def hardware_inhibitor_checks_failed(
    hardware_checks_failed: bool, failures: list, hardware_check: bool
):
    # ask if an update can be performed through dbus notifications
    if check_for_updates(hardware_checks_failed) and not hardware_check:
        log.info("Harware checks failed, but update is available")
        ask_for_updates()
    # notify systemd that the checks have failed,
    # systemd will try to rerun the unit
    exception_log = "\n - ".join(failures)
    raise Exception(f"update failed to pass checks: \n - {exception_log}")


def run_update_scripts(root_dir: str):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            full_path = root_dir + str(file)
            executable = os.access(full_path, os.X_OK)
            if executable:
                log.info(f"Running update script: {full_path}")
                out = subprocess.run(
                    [full_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                if out.returncode != 0:
                    log.info(f"{full_path} returned error code: {out.returncode}")
                    log.info(f"Program output: \n {out.stdout.decode('utf-8')}")
                    notify(
                        "System Updater",
                        f"Error in update script: {file}, check logs for more info",
                    )
            else:
                log.info(f"could not execute file {full_path}")


def run_updates(args):
    root_dir = "/etc/ublue-update.d"

    """Wait on any existing transactions to complete before updating"""
    transaction_wait()

    process_uid = os.getuid()
    if process_uid == 0:
        notify(
            "System Updater",
            "System passed checks, updating ...",
        )
        user_uids = []
        if not args.system:
            for user in pwd.getpwall():
                if "/home" in user.pw_dir:
                    user_uids.append(user.pw_uid)

        run_update_scripts(root_dir + "/system/")
        for user_uid in user_uids:
            xdg_runtime_dir = get_xdg_runtime_dir(user_uid)
            user = pwd.getpwuid(user_uid)
            log.info(
                f"""
                Running update for user:
                'user.pw_name}',
                update script directory: '{root_dir}/user'
                """
            )

            subprocess.run(
                [
                    "sudo",
                    "-u",
                    f"{user.pw_name}",
                    "DISPLAY=:0",
                    f"XDG_RUNTIME_DIR={xdg_runtime_dir}",
                    f"DBUS_SESSION_BUS_ADDRESS=unix:path={xdg_runtime_dir}/bus",
                    "/usr/bin/ublue-update",
                    "-f",
                ]
            )
            notify(
                "System Updater",
                "System update complete, reboot for changes to take effect",
            )
            log.info("System update complete")
    else:
        if args.system:
            raise Exception(
                "ublue-update needs to be run as root to perform system updates!"
            )
        run_update_scripts(root_dir + "/user/")
    os._exit(0)


dbus_notify: bool = load_value("notify", "dbus_notify")

# setup logging
logging.basicConfig(
    format="[%(asctime)s] %(name)s:%(levelname)s | %(message)s",
    level=os.getenv("UBLUE_LOG", default=logging.INFO),
)
log = logging.getLogger(__name__)

cli_args = None


def main():

    # setup argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="force manual update, skipping update checks",
    )
    parser.add_argument(
        "-c", "--check", action="store_true", help="run update checks and exit"
    )
    parser.add_argument(
        "-u",
        "--updatecheck",
        action="store_true",
        help="check for updates and exit",
    )
    parser.add_argument(
        "-w",
        "--wait",
        action="store_true",
        help="wait for transactions to complete and exit",
    )
    parser.add_argument(
        "--system",
        action="store_true",
        help="only run system updates (requires root)",
    )
    cli_args = parser.parse_args()
    hardware_checks_failed = False

    if cli_args.wait:
        transaction_wait()
        os._exit(0)

    if not cli_args.force and not cli_args.updatecheck:
        hardware_checks_failed, failures = check_hardware_inhibitors()
        if hardware_checks_failed:
            hardware_inhibitor_checks_failed(
                hardware_checks_failed,
                failures,
                cli_args.check,
            )
        if cli_args.check:
            os._exit(0)

    if cli_args.updatecheck:
        update_available = check_for_updates(False)
        if not update_available:
            raise Exception("Update not available")
        os._exit(0)

    # system checks passed
    log.info("System passed all update checks")
    run_updates(cli_args)

import os
import subprocess
import logging
import argparse
import pwd

from ublue_update.update_checks.system import system_update_check
from ublue_update.update_checks.wait import transaction_wait
from ublue_update.update_inhibitors.hardware import check_hardware_inhibitors
from ublue_update.config import load_value


def notify(title: str, body: str, actions: list = [], urgency: str = "normal"):
    if not dbus_notify:
        return
    args = [
        "/usr/bin/notify-send",
        title,
        body,
        "--app-name=Universal Blue Updater",
        "--icon=software-update-available-symbolic",
        f"--urgency={urgency}",
    ]
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
        run_updates(args)


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


def run_user_updates(process_uid: int, user_uid: int, root_dir: str):
    if process_uid != 0 and user_uid != process_uid:
        if user_uid == 0:
            notify(
                "System Updater",
                "ublue-update needs root for system updates!",
            )
            raise Exception("ublue-update needs root for system updates!")
        return

    user_name = pwd.getpwuid(user_uid).pw_name
    log.info(f"Running update for user: '{user_name}', update script directory: '{root_dir}'")
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            full_path = root_dir + str(file)
            executable = os.access(full_path, os.X_OK)
            if executable:
                log.info(f"Running update script: {full_path}")
                out = subprocess.run(
                    ["/usr/bin/sudo","-u",f"{user_name}",full_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
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
    notify(
        "System Updater",
        "System passed checks, updating ...",
    )
    root_dir = "/etc/ublue-update.d"

    """Wait on any existing transactions to complete before updating"""
    transaction_wait()
    user_uids=[]
    not_specified=(not args.user and not args.system)

    if not_specified or args.user:
        for user in pwd.getpwall():
            if "/home" in user.pw_dir:
                user_uids.append(user.pw_uid)
    process_uid = os.getuid()
    if not_specified or args.system:
        run_user_updates(process_uid, 0, root_dir + "/system/")

    for user_uid in user_uids:
        run_user_updates(process_uid, user_uid, root_dir + "/user/")


    notify(
        "System Updater",
        "System update complete, reboot for changes to take effect",
    )
    log.info("System update complete")
    os._exit(0)

dbus_notify: bool = load_value("notify", "dbus_notify")

# setup logging
logging.basicConfig(
    format="[%(asctime)s] %(name)s:%(levelname)s | %(message)s",
    level=os.getenv("UBLUE_LOG", default=logging.INFO),
)
log = logging.getLogger(__name__)

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
        "--user",
        action="store_true",
        help="run user updates",
    )
    parser.add_argument(
        "--system",
        action="store_true",
        help="run system updates",
    )
    args = parser.parse_args()
    hardware_checks_failed = False

    if args.wait:
        transaction_wait()
        os._exit(0)

    if not args.force and not args.updatecheck:
        hardware_checks_failed, failures = check_hardware_inhibitors()
        if hardware_checks_failed:
            hardware_inhibitor_checks_failed(
                hardware_checks_failed,
                failures,
                args.check,
            )
        if args.check:
            os._exit(0)

    if args.updatecheck:
        update_available = check_for_updates(False)
        if not update_available:
            raise Exception("Update not available")
        os._exit(0)

    # system checks passed
    log.info("System passed all update checks")
    run_updates(args)

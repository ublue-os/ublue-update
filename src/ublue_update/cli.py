import os
import subprocess
import logging
import argparse

from ublue_update.update_checks.system import (
    system_update_check,
    pending_deployment_check,
)
from ublue_update.update_checks.wait import transaction_wait
from ublue_update.update_inhibitors.hardware import check_hardware_inhibitors
from ublue_update.update_inhibitors.custom import check_custom_inhibitors
from ublue_update.config import cfg
from ublue_update.session import get_active_users
from ublue_update.filelock import acquire_lock, release_lock


def notify(title: str, body: str, actions: list = [], urgency: str = "normal"):
    if not cfg.dbus_notify:
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
    if actions != []:
        for action in actions:
            args.append(f"--action={action}")
    if process_uid == 0:
        users = []
        try:
            users = get_active_users()
        except KeyError as e:
            log.error("failed to get active logind session info", e)
        for user in users:
            user_args = [
                "/usr/bin/systemd-run",
                "--user",
                "--machine",
                f"{user[1]}@",  # magic number, corresponds to user name in ListUsers (see session.py)
                "--pipe",
                "--quiet",
            ]
            user_args += args
            out = subprocess.run(user_args, capture_output=True)
            if actions != []:
                return out
        return
    out = subprocess.run(args, capture_output=True)
    return out


def ask_for_updates(system):
    if not cfg.dbus_notify:
        return
    out = notify(
        "System Updater",
        "Update available, but system checks failed. Update now?",
        ["universal-blue-update-confirm=Confirm"],
        "critical",
    )
    if out is None:
        return
    # if the user has confirmed
    if "universal-blue-update-confirm" in out.stdout.decode("utf-8"):
        run_updates(system, True)


def inhibitor_checks_failed(
    failures: list, hardware_check: bool, system_update_available: bool, system: bool
):
    # ask if an update can be performed through dbus notifications
    if system_update_available and not hardware_check:
        log.info("Precondition checks failed, but update is available")
        ask_for_updates(system)
    # notify systemd that the checks have failed,
    # systemd will try to rerun the unit
    exception_log = "\n - ".join(failures)
    raise Exception(f"update failed to pass checks: \n - {exception_log}")


def run_updates(system, system_update_available):
    process_uid = os.getuid()
    filelock_path = "/run/ublue-update.lock"
    if process_uid != 0:
        xdg_runtime_dir = os.environ.get("XDG_RUNTIME_DIR")
        if os.path.isdir(xdg_runtime_dir):
            filelock_path = f"{xdg_runtime_dir}/ublue-update.lock"
    fd = acquire_lock(filelock_path)
    if fd is None:
        raise Exception("updates are already running for this user")

    """Wait on any existing transactions to complete before updating"""
    transaction_wait()

    if process_uid == 0:
        if system_update_available:
            # Notify about a full system update but not about only
            # distrobox and flatpak updates
            notify(
                "System Updater",
                "System passed checks, updating ...",
            )
        users = []
        try:
            users = get_active_users()
        except KeyError as e:
            log.error("failed to get active logind session info", e)

        if system:
            users = []

        """System"""
        # remove backwards compat warnings in topgrade (requires user confirmation without this env var)
        os.environ["TOPGRADE_SKIP_BRKC_NOTIFY"] = "true"
        out = subprocess.run(
            [
                "/usr/bin/topgrade",
                "--config",
                "/usr/share/ublue-update/topgrade-system.toml",
            ],
            capture_output=True,
        )
        log.debug(out.stdout.decode("utf-8"))

        if out.returncode != 0:
            print(f"topgrade returned code {out.returncode}, program output:")
            print(out.stdout.decode("utf-8"))
            os._exit(out.returncode)

        """Users"""
        for user in users:
            log.info(
                f"""Running update for user: '{user[1]}'"""
            )  # magic number, corresponds to username (see session.py)
            out = subprocess.run(
                [
                    "/usr/bin/systemd-run",
                    "--setenv=TOPGRADE_SKIP_BRKC_NOTIFY=true",
                    "--user",
                    "--machine",
                    f"{user[1]}@",
                    "--pipe",
                    "--quiet",
                    "/usr/bin/topgrade",
                    "--config",
                    "/usr/share/ublue-update/topgrade-user.toml",
                ],
                capture_output=True,
            )
            log.debug(out.stdout.decode("utf-8"))
        log.info("System update complete")
        if pending_deployment_check() and system_update_available and cfg.dbus_notify:
            out = notify(
                "System Updater",
                "System update complete, pending changes will take effect after reboot. Reboot now?",
                ["universal-blue-update-reboot=Reboot Now"],
            )
            # if the user has confirmed the reboot
            if "universal-blue-update-reboot" in out.stdout.decode("utf-8"):
                subprocess.run(["systemctl", "reboot"])
    else:
        if system:
            raise Exception(
                "ublue-update needs to be run as root to perform system updates!"
            )
    release_lock(fd)
    os._exit(0)


# setup logging
logging.basicConfig(
    format="[%(asctime)s] %(name)s:%(levelname)s | %(message)s",
    level=os.getenv("UBLUE_LOG", default="INFO").upper(),
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
    parser.add_argument("--config", help="use the specified config file")
    parser.add_argument(
        "--system",
        action="store_true",
        help="only run system updates (requires root)",
    )
    cli_args = parser.parse_args()

    # Load the configuration file
    cfg.load_config(cli_args.config)

    if cli_args.wait:
        transaction_wait()
        os._exit(0)

    system_update_available: bool = system_update_check()
    if not cli_args.force and not cli_args.updatecheck:
        hw_checks_failed, hw_failures = check_hardware_inhibitors()
        cs_checks_failed, cs_failures = check_custom_inhibitors()

        checks_failed = hw_checks_failed or cs_checks_failed
        failures = hw_failures + cs_failures

        if checks_failed:
            inhibitor_checks_failed(
                failures,
                cli_args.check,
                system_update_available,
                cli_args.system,
            )
        if cli_args.check:
            os._exit(0)

    if cli_args.updatecheck:
        if not system_update_available:
            raise Exception("Update not available")
        os._exit(0)

    # system checks passed
    log.info("System passed all update checks")
    try:
        run_updates(cli_args.system, system_update_available)
    except Exception as e:
        log.info(f"Failed to update: {e}")
        os._exit(1)

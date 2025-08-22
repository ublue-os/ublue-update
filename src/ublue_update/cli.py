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
from ublue_update.session import get_active_users, run_uid
from ublue_update.update_drivers.brew import brew_update
from ublue_update.filelock import acquire_lock, release_lock


def notify(
    title: str, body: str, actions: list = [], urgency: str = "normal"
) -> subprocess.CompletedProcess[bytes] | None:
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
    # If root run per user:
    if process_uid == 0:
        users = []
        try:
            users = get_active_users()
        except KeyError as e:
            log.error("failed to get active logind session info", e)
        out: subprocess.CompletedProcess[bytes] | None = None
        for user in users:
            out = run_uid(user[0], args)
        return out

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
        run_updates(system, True, False)


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


def run_updates(system: bool, system_update_available: bool, dry_run: bool):
    process_uid = os.getuid()
    filelock_path = "/run/ublue-update.lock"
    if process_uid != 0:
        xdg_runtime_dir = os.environ.get("XDG_RUNTIME_DIR")
        if xdg_runtime_dir is not None and os.path.isdir(xdg_runtime_dir):
            filelock_path = f"{xdg_runtime_dir}/ublue-update.lock"
    fd = acquire_lock(filelock_path)
    if fd is None:
        raise Exception("updates are already running for this user")

    """Wait on any existing transactions to complete before updating"""
    # remove backwards compat warnings in topgrade (requires user confirmation without this env var)
    os.environ["TOPGRADE_SKIP_BRKC_NOTIFY"] = "true"
    topgrade_args = [
        "/usr/bin/topgrade",
    ]

    if dry_run:
        topgrade_args.append("--dry-run")
        # disable toolbox during dry run because it doesn't want to run in the container: github.com/containers/toolbox/issues/989
        topgrade_args.extend(["--disable", "toolbx"])
    else:
        transaction_wait()

    topgrade_system = topgrade_args + [
        "--config",
        "/usr/share/ublue-update/topgrade-system.toml",
    ]
    topgrade_user = topgrade_args + [
        "--config",
        "/usr/share/ublue-update/topgrade-user.toml",
    ]

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
        out = subprocess.run(
            topgrade_system,
            capture_output=True,
        )
        log.debug(out.stdout.decode("utf-8"))

        if out.returncode != 0:
            log.error(f"topgrade returned code {out.returncode}, program output:")
            log.error(out.stderr.decode("utf-8"))
            os._exit(out.returncode)

        """Users"""
        for user in users:

            log.info(
                f"""Running update for user: '{user[1]}'"""
            )  # magic number, corresponds to username (see session.py)

            out = run_uid(
                user[0], ["--setenv=TOPGRADE_SKIP_BRKC_NOTIFY=true"] + topgrade_user
            )  # uid for user (session.py)
            log.debug(out.stdout.decode("utf-8"))
        brew_update(dry_run)
        log.info("System update complete")
        if pending_deployment_check() and system_update_available and cfg.dbus_notify:
            out = notify(
                "System Updater",
                "System update complete, pending changes will take effect after reboot. Reboot now?",
                ["universal-blue-update-reboot=Reboot Now"],
            )
            # if the user has confirmed the reboot
            if out is not None and "universal-blue-update-reboot" in out.stdout.decode(
                "utf-8"
            ):
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
    parser.add_argument("--config", help="use the specified config file")
    parser.add_argument(
        "--system",
        action="store_true",
        help="only run system updates (requires root)",
    )
    parser.add_argument(
        "--check", action="store_true", help="run update checks and exit"
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
        "--dry-run",
        action="store_true",
        help="dry run ublue-update",
    )
    cli_args = parser.parse_args()

    # Load the configuration file

    cfg.load_config(cli_args.config)

    if cli_args.dry_run:
        # "dry run" the hardware tests as well
        _, _ = check_hardware_inhibitors()
        _, _ = check_custom_inhibitors()
        # run the update function with "dry run" set to true
        run_updates(False, True, True)
        os._exit(0)

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
        run_updates(cli_args.system, system_update_available, False)
    except Exception as e:
        log.info(f"Failed to update: {e}")
        os._exit(1)

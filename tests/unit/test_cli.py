import pytest
import sys
import os
from unittest.mock import patch, MagicMock, mock_open

# Add the src directory to the sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from ublue_update.cli import (
    notify,
    ask_for_updates,
    inhibitor_checks_failed,
    run_updates,
)


@patch("ublue_update.cli.cfg")
@patch("ublue_update.cli.os")
@patch("ublue_update.cli.log")
@patch("ublue_update.cli.subprocess.run")
def test_notify_no_dbus_notify(mock_run, mock_log, mock_os, mock_cfg):
    mock_cfg.dbus_notify = False
    assert notify("test_title", "test_body") == None


@patch("ublue_update.cli.cfg")
@patch("ublue_update.cli.os")
@patch("ublue_update.cli.log")
@patch("ublue_update.cli.subprocess.run")
def test_notify_uid_user(mock_run, mock_log, mock_os, mock_cfg):
    title = "test title"
    body = "test body"
    mock_cfg.dbus_notify = True
    mock_os.getuid.return_value = 1001
    notify(title, body)
    mock_run.assert_called_once_with(
        [
            "/usr/bin/notify-send",
            title,
            body,
            "--app-name=Universal Blue Updater",
            "--icon=software-update-available-symbolic",
            f"--urgency=normal",
        ],
        capture_output=True,
    )


@patch("ublue_update.cli.cfg")
def test_ask_for_updates_no_dbus_notify(mock_cfg):
    mock_cfg.dbus_notify = False
    assert ask_for_updates(True) == None


@patch("ublue_update.cli.cfg")
@patch("ublue_update.cli.notify")
def test_ask_for_updates_notify_none(mock_notify, mock_cfg):
    mock_cfg.dbus_notify = True
    mock_notify.return_value = None
    assert ask_for_updates(True) == None
    mock_notify.assert_called_once_with(
        "System Updater",
        "Update available, but system checks failed. Update now?",
        ["universal-blue-update-confirm=Confirm"],
        "critical",
    )


@patch("ublue_update.cli.cfg")
@patch("ublue_update.cli.notify")
@patch("ublue_update.cli.run_updates")
def test_ask_for_updates_system(mock_run_updates, mock_notify, mock_cfg):
    mock_cfg.dbus_notify = True
    mock_notify.return_value = MagicMock(stdout=b"universal-blue-update-confirm")
    system = True
    ask_for_updates(system)
    mock_notify.assert_called_once_with(
        "System Updater",
        "Update available, but system checks failed. Update now?",
        ["universal-blue-update-confirm=Confirm"],
        "critical",
    )
    mock_run_updates.assert_called_once_with(system, True)


@patch("ublue_update.cli.cfg")
@patch("ublue_update.cli.notify")
@patch("ublue_update.cli.run_updates")
def test_ask_for_updates_user(mock_run_updates, mock_notify, mock_cfg):
    mock_cfg.dbus_notify = True
    mock_notify.return_value = MagicMock(stdout=b"universal-blue-update-confirm")
    system = False
    ask_for_updates(system)
    mock_notify.assert_called_once_with(
        "System Updater",
        "Update available, but system checks failed. Update now?",
        ["universal-blue-update-confirm=Confirm"],
        "critical",
    )
    mock_run_updates.assert_called_once_with(system, True)


def test_inhibitor_checks_failed():
    failure_message1 = "Failure 1"
    failure_message2 = "Failure 2"
    with pytest.raises(Exception, match=f"{failure_message1}\n - {failure_message2}"):
        inhibitor_checks_failed([failure_message1, failure_message2], True, True, True)


@patch("ublue_update.cli.ask_for_updates")
@patch("ublue_update.cli.log")
def test_inhibitor_checks_failed_no_hw_check(mock_log, mock_ask_for_updates):
    failure_message1 = "Failure 1"
    failure_message2 = "Failure 2"
    with pytest.raises(Exception, match=f"{failure_message1}\n - {failure_message2}"):
        inhibitor_checks_failed([failure_message1, failure_message2], False, True, True)
        mock_log.assert_called_once_with(
            "Precondition checks failed, but update is available"
        )
        mock_ask_for_updates.assert_called_once()


@patch("ublue_update.cli.os")
@patch("ublue_update.cli.acquire_lock")
def test_run_updates_user_in_progress(mock_acquire_lock, mock_os):
    mock_os.getuid.return_value = 1001
    mock_os.environ.get.return_value = "/path/to"
    mock_os.path.isdir.return_value = True
    mock_acquire_lock.return_value = None
    with pytest.raises(Exception, match="updates are already running for this user"):
        run_updates(False, True)


@patch("ublue_update.cli.os")
@patch("ublue_update.cli.acquire_lock")
@patch("ublue_update.cli.transaction_wait")
def test_run_updates_user_system(mock_transaction_wait, mock_acquire_lock, mock_os):
    mock_os.getuid.return_value = 1001
    mock_acquire_lock.return_value = 3
    mock_os.path.isdir.return_value = False
    with pytest.raises(
        Exception,
        match="ublue-update needs to be run as root to perform system updates!",
    ):
        run_updates(True, True)


@patch("ublue_update.cli.os")
@patch("ublue_update.cli.acquire_lock")
@patch("ublue_update.cli.transaction_wait")
@patch("ublue_update.cli.release_lock")
def test_run_updates_user_no_system(
    mock_release_lock, mock_transaction_wait, mock_acquire_lock, mock_os
):
    fd = 3
    mock_os.getuid.return_value = 1001
    mock_acquire_lock.return_value = fd
    mock_os.path.isdir.return_value = False
    run_updates(False, True)
    mock_release_lock.assert_called_once_with(fd)


@patch("ublue_update.cli.os")
@patch("ublue_update.cli.get_active_sessions")
@patch("ublue_update.cli.acquire_lock")
@patch("ublue_update.cli.transaction_wait")
@patch("ublue_update.cli.subprocess.run")
@patch("ublue_update.cli.log")
@patch("ublue_update.cli.pending_deployment_check")
@patch("ublue_update.cli.cfg")
@patch("ublue_update.cli.release_lock")
@patch("ublue_update.cli.notify")
def test_run_updates_system(
    mock_notify,
    mock_release_lock,
    mock_cfg,
    mock_pending_deployment_check,
    mock_log,
    mock_run,
    mock_transaction_wait,
    mock_acquire_lock,
    mock_get_active_sesions,
    mock_os,
):
    mock_os.getuid.return_value = 0
    mock_acquire_lock.return_value = 3
    output = MagicMock(stdout=b"test log")
    output.returncode = 1
    mock_run.return_value = output
    mock_pending_deployment_check.return_value = True
    mock_cfg.dbus_notify.return_value = True
    run_updates(True, True)
    mock_notify.assert_any_call(
        "System Updater",
        "System passed checks, updating ...",
    )
    mock_run.assert_any_call(
        [
            "/usr/bin/topgrade",
            "--config",
            "/usr/share/ublue-update/topgrade-system.toml",
        ],
        capture_output=True,
    )
    mock_notify.assert_any_call(
        "System Updater",
        "System update complete, pending changes will take effect after reboot. Reboot now?",
        ["universal-blue-update-reboot=Reboot Now"],
    )


@patch("ublue_update.cli.os")
@patch("ublue_update.cli.get_active_sessions")
@patch("ublue_update.cli.acquire_lock")
@patch("ublue_update.cli.transaction_wait")
@patch("ublue_update.cli.subprocess.run")
@patch("ublue_update.cli.log")
@patch("ublue_update.cli.pending_deployment_check")
@patch("ublue_update.cli.cfg")
@patch("ublue_update.cli.release_lock")
@patch("ublue_update.cli.notify")
def test_run_updates_system_reboot(
    mock_notify,
    mock_release_lock,
    mock_cfg,
    mock_pending_deployment_check,
    mock_log,
    mock_run,
    mock_transaction_wait,
    mock_acquire_lock,
    mock_get_active_sesions,
    mock_os,
):
    mock_os.getuid.return_value = 0
    mock_acquire_lock.return_value = 3
    output = MagicMock(stdout=b"test log")
    output.returncode = 1
    mock_run.return_value = output
    mock_pending_deployment_check.return_value = True
    mock_cfg.dbus_notify.return_value = True
    reboot = MagicMock(stdout=b"universal-blue-update-reboot")
    mock_notify.side_effect = [None, reboot]
    run_updates(True, True)
    mock_notify.assert_any_call(
        "System Updater",
        "System passed checks, updating ...",
    )
    mock_run.assert_any_call(
        [
            "/usr/bin/topgrade",
            "--config",
            "/usr/share/ublue-update/topgrade-system.toml",
        ],
        capture_output=True,
    )
    mock_notify.assert_any_call(
        "System Updater",
        "System update complete, pending changes will take effect after reboot. Reboot now?",
        ["universal-blue-update-reboot=Reboot Now"],
    )
    mock_run.assert_any_call(["systemctl", "reboot"])

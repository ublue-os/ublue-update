import os
import sys
from unittest.mock import patch

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from ublue_update.update_drivers.brew import (
    BREW_PATH,
    detect_user,
    brew_update,
    BREW_PREFIX,
    BREW_CELLAR,
    BREW_REPO,
)


@patch("os.path.isdir")
@patch("os.stat")
def test_detect_user_success(mock_stat, mock_isdir):
    mock_isdir.return_value = True
    mock_stat.return_value.st_uid = 1001

    assert detect_user() == 1001

    mock_isdir.assert_called_once_with(BREW_PREFIX)
    mock_stat.assert_called_once_with(BREW_PREFIX)


@patch("os.path.isdir")
def test_detect_user_failure(mock_isdir):
    mock_isdir.return_value = False

    assert detect_user() == -1

    mock_isdir.assert_called_once_with(BREW_PREFIX)


@patch("ublue_update.update_drivers.brew.run_uid")
@patch("os.environ", {"PATH": "/usr/bin"})
@patch("os.path.isdir")
@patch("os.stat")
@patch("ublue_update.update_drivers.brew.log")
def test_brew_update(mock_log, mock_stat, mock_isdir, mock_run_uid):
    # Setup
    mock_isdir.return_value = True
    mock_stat.return_value.st_uid = 1001
    mock_run_uid.return_value.returncode = 0  # Simulate a successful command

    brew_update(True)

    # Test that brew_update returns early when dry_run is True
    mock_run_uid.assert_not_called()
    mock_log.info.assert_not_called()

    brew_update(False)
    env = [
        f"--setenv=HOMEBREW_PREFIX='{BREW_PREFIX}'",
        f"--setenv=HOMEBREW_CELLAR='{BREW_CELLAR}'",
        f"--setenv=HOMEBREW_REPOSITORY='{BREW_REPO}'",
    ]

    mock_run_uid.assert_any_call(1001, env + [f"{BREW_PATH}", "update"])
    mock_run_uid.assert_any_call(1001, env + [f"{BREW_PATH}", "upgrade"])


@patch("ublue_update.update_drivers.brew.run_uid")
@patch("os.environ", {"PATH": "/usr/local/bin"})
@patch("os.path.isdir")
@patch("os.stat")
@patch("ublue_update.update_drivers.brew.log")
def test_brew_update_failure(mock_log, mock_stat, mock_isdir, mock_run_uid):
    mock_isdir.return_value = True
    mock_stat.return_value.st_uid = 1001
    mock_run_uid.return_value.returncode = (
        1  # Simulate a failure in the `brew update` command
    )
    mock_run_uid.return_value.stderr= b"Error"

    brew_update(False)

    mock_log.error.assert_any_call("Error")


@patch("ublue_update.update_drivers.brew.run_uid")
@patch("os.environ", {"PATH": "/usr/local/bin"})
@patch("os.path.isdir")
@patch("os.stat")
@patch("ublue_update.update_drivers.brew.log")
def test_brew_update_upgrade_failure(mock_log, mock_stat, mock_isdir, mock_run_uid):
    mock_isdir.return_value = True
    mock_stat.return_value.st_uid = 1001
    mock_run_uid.return_value.returncode = 0  # Simulate a successful `brew update`
    mock_run_uid.return_value.stdout = b"Update complete"

    mock_run_uid.return_value.returncode = 1  # Simulate a failure during `brew upgrade`
    mock_run_uid.return_value.stderr = b"Error"

    brew_update(False)

    mock_log.error.assert_any_call("Error")

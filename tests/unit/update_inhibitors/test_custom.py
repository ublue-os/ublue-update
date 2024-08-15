import pytest
import sys
import os
from unittest.mock import patch, MagicMock, mock_open

# Add the src directory to the sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from ublue_update.update_inhibitors.custom import (
    run_custom_check_script,
    run_custom_check_scripts,
    check_custom_inhibitors,
)


@patch("ublue_update.update_inhibitors.custom.log")
@patch("ublue_update.update_inhibitors.custom.subprocess.run")
def test_run_custom_check_script_pass(mock_run, mock_log):
    script = {
        "run": "echo Hello World",
        "shell": "/bin/bash",
    }
    mock_result = MagicMock(stdout=b"Script ran successfully.")
    mock_run.return_value = mock_result
    mock_result.returncode = 0
    result = run_custom_check_script(script)
    assert result["passed"]
    mock_run.assert_called_once_with(
        ["/bin/bash", "-c", "echo Hello World"],
        capture_output=True,
        text=True,
        check=False,
    )


@patch("ublue_update.update_inhibitors.custom.log")
@patch("ublue_update.update_inhibitors.custom.subprocess.run")
def test_run_custom_check_script_fail(mock_run, mock_log):
    script = {
        "run": "echo Hello World",
        "shell": "/bin/bash",
    }
    mock_result = MagicMock(stdout=b"Script ran unsuccessfully.")
    mock_run.return_value = mock_result
    mock_result.returncode = 1
    result = run_custom_check_script(script)
    assert not result["passed"]
    mock_run.assert_called_once_with(
        ["/bin/bash", "-c", "echo Hello World"],
        capture_output=True,
        text=True,
        check=False,
    )


def test_run_custom_check_script_run_no_shell_exc():
    with pytest.raises(
        Exception,
        match="checks.scripts.*: 'shell' must be specified when 'run' is used",
    ):
        run_custom_check_script({"run": "some_command"})


def test_run_custom_check_script_run_and_file_exc():
    with pytest.raises(
        Exception,
        match="checks.scripts.*: Only one of 'run' and 'file' must be set for a given script",
    ):
        run_custom_check_script(
            {"run": "some_command", "file": "some_file", "shell": "some_shell"}
        )


@patch("ublue_update.update_inhibitors.custom.cfg")
@patch("ublue_update.update_inhibitors.custom.run_custom_check_script")
def test_run_custom_check_scripts(mock_run_custom_check_script, mock_cfg):
    script = "test_script.sh"
    result = {"passed": True, "message": "message"}
    mock_cfg.custom_check_scripts = [script]
    mock_run_custom_check_script.return_value = result

    assert run_custom_check_scripts() == [result]
    mock_run_custom_check_script.assert_called_once_with(script)


@patch("ublue_update.update_inhibitors.custom.run_custom_check_scripts")
@patch("ublue_update.update_inhibitors.custom.log")
def test_check_custom_inhibitors_passed(mock_log, mock_run_custom_check_scripts):
    mock_run_custom_check_scripts.return_value = [
        {"passed": True, "message": "message1"},
        {"passed": True, "message": "message2"},
    ]
    result = check_custom_inhibitors()
    assert not result[0]
    assert result[1] == []
    mock_log.info.assert_called_once_with("System passed custom checks")


@patch("ublue_update.update_inhibitors.custom.run_custom_check_scripts")
@patch("ublue_update.update_inhibitors.custom.log")
def test_check_custom_inhibitors_failed(mock_log, mock_run_custom_check_scripts):
    mock_run_custom_check_scripts.return_value = [
        {"passed": False, "message": "message1"},
        {"passed": True, "message": "message2"},
    ]
    result = check_custom_inhibitors()
    assert result[0]
    assert result[1] == ["message1"]
    mock_log.info.assert_not_called()

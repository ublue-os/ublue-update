import sys
import os
from unittest.mock import patch, MagicMock

# Add the src directory to the sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../src"))
)

from ublue_update.update_checks.system import (
    skopeo_inspect,
    system_update_check,
    pending_deployment_check,
)


@patch("ublue_update.update_checks.system.run")
def test_skopeo_inspect(mock_run):
    test_input = "latest"
    test_output = '{"Digest": "mocked_digest"}'
    mock_skopeo_out = MagicMock()
    mock_skopeo_out.stdout = test_output

    mock_run.return_value = mock_skopeo_out
    assert skopeo_inspect(test_input) == "mocked_digest"
    mock_run.assert_called_once_with(
        ["skopeo", "inspect", test_input], capture_output=True
    )


@patch("ublue_update.update_checks.system.run")
@patch("ublue_update.update_checks.system.skopeo_inspect")
@patch("ublue_update.update_checks.system.log")
def test_system_update_check(mock_log, mock_skopeo_inspect, mock_run):
    # Test when the system update is available
    mock_run.return_value.stdout = '{"deployments": [{"base-commit-meta": {"ostree.manifest-digest": "digest1"}, "container-image-reference": "image:tag"}]}'
    mock_skopeo_inspect.return_value = "digest2"
    mock_log.info = MagicMock()
    mock_log.error = MagicMock()

    assert system_update_check()
    mock_log.info.assert_called_with("System update available.")
    mock_run.assert_called_once_with(
        ["rpm-ostree", "status", "--json"], capture_output=True
    )
    mock_skopeo_inspect.assert_called_once_with("docker://tag")


@patch("ublue_update.update_checks.system.run")
@patch("ublue_update.update_checks.system.skopeo_inspect")
@patch("ublue_update.update_checks.system.log")
def test_system_update_check_no_update(mock_log, mock_skopeo_inspect, mock_run):
    # Test when there is no update available
    mock_run.return_value.stdout = '{"deployments": [{"base-commit-meta": {"ostree.manifest-digest": "digest1"}, "container-image-reference": "image:tag"}]}'
    mock_skopeo_inspect.return_value = "digest1"
    mock_log.info = MagicMock()
    mock_log.error = MagicMock()

    assert not system_update_check()
    mock_log.info.assert_called_with("No system update available.")
    mock_run.assert_called_once_with(
        ["rpm-ostree", "status", "--json"], capture_output=True
    )
    mock_skopeo_inspect.assert_called_once_with("docker://tag")


@patch("ublue_update.update_checks.system.run")
@patch("ublue_update.update_checks.system.log")
def test_system_update_check_json_error(mock_log, mock_run):
    # Test handling of JSON decoding errors
    mock_run.return_value.stdout = "invalid json"
    mock_log.info = MagicMock()
    mock_log.error = MagicMock()

    assert not system_update_check()
    mock_log.error.assert_called_with(
        "update check failed, system isn't managed by rpm-ostree container native"
    )
    mock_run.assert_called_once_with(
        ["rpm-ostree", "status", "--json"], capture_output=True
    )


@patch("ublue_update.update_checks.system.run")
def test_pending_deployment_check(mock_run):
    # Test when there is no pending deployment
    mock_run.return_value.returncode = 77

    assert pending_deployment_check()
    mock_run.assert_called_once_with(
        ["rpm-ostree", "status", "--pending-exit-77"], capture_output=True
    )


@patch("ublue_update.update_checks.system.run")
def test_pending_deployment_check_with_pending(mock_run):
    # Test when there is a pending deployment
    mock_run.return_value.returncode = 1

    assert not pending_deployment_check()
    mock_run.assert_called_once_with(
        ["rpm-ostree", "status", "--pending-exit-77"], capture_output=True
    )

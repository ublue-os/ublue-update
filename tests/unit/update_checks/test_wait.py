import sys
import os
from unittest.mock import patch, MagicMock
from ublue_update.update_checks.wait import transaction, transaction_wait

# Add the src directory to the sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../src"))
)


@patch("ublue_update.update_checks.wait.run")
@patch("ublue_update.update_checks.wait.log")
def test_transaction_success(mock_log, mock_run):
    # Mock subprocess.run to return valid JSON output
    mock_run.return_value = MagicMock(stdout='{"transaction": "some_transaction_data"}')
    mock_log.error = MagicMock()

    result = transaction()

    assert result == "some_transaction_data"
    mock_run.assert_called_once_with(
        ["/usr/bin/rpm-ostree", "status", "--json"], capture_output=True
    )
    mock_log.error.assert_not_called()


@patch("ublue_update.update_checks.wait.run")
@patch("ublue_update.update_checks.wait.log")
def test_transaction_json_decode_error(mock_log, mock_run):
    # Mock subprocess.run to return invalid JSON output
    mock_run.return_value = MagicMock(stdout="invalid json")
    mock_log.error = MagicMock()

    result = transaction()

    assert result is None
    mock_run.assert_called_once_with(
        ["/usr/bin/rpm-ostree", "status", "--json"], capture_output=True
    )
    mock_log.error.assert_called_once_with(
        "can't get transaction, system not managed with rpm-ostree container native"
    )


@patch("ublue_update.update_checks.wait.run")
@patch("ublue_update.update_checks.wait.log")
def test_transaction_key_error(mock_log, mock_run):
    # Mock subprocess.run to return JSON with missing 'transaction' key
    mock_run.return_value = MagicMock(stdout='{"some_key": "some_value"}')
    mock_log.error = MagicMock()

    result = transaction()

    assert result is None
    mock_run.assert_called_once_with(
        ["/usr/bin/rpm-ostree", "status", "--json"], capture_output=True
    )
    mock_log.error.assert_called_once_with(
        "can't get transaction, system not managed with rpm-ostree container native"
    )


@patch("ublue_update.update_checks.wait.transaction")
@patch("ublue_update.update_checks.wait.sleep", return_value=None)
def test_transaction_wait(mock_sleep, mock_transaction):
    # Mock transaction() to return None eventually
    mock_transaction.side_effect = [1, 2, None]

    transaction_wait()

    assert mock_transaction.call_count == 3
    mock_sleep.assert_called_with(1)


@patch("ublue_update.update_checks.wait.transaction")
@patch("ublue_update.update_checks.wait.sleep", return_value=None)
def test_transaction_wait_no_sleep(mock_sleep, mock_transaction):
    # Mock transaction() to return None immediately
    mock_transaction.return_value = None

    transaction_wait()

    mock_transaction.assert_called_once()
    mock_sleep.assert_not_called()

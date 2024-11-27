import sys
import os
import fcntl
from unittest.mock import patch

# Add the src directory to the sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from ublue_update.filelock import acquire_lock, release_lock


@patch("ublue_update.filelock.os.open")
@patch("ublue_update.filelock.fcntl.flock")
@patch("ublue_update.filelock.os.close")
@patch("ublue_update.filelock.time.sleep", return_value=None)
@patch("ublue_update.filelock.log")
def test_acquire_lock_success(mock_log, mock_sleep, mock_close, mock_flock, mock_open):
    mock_fd = 3
    mock_open.return_value = mock_fd
    mock_flock.return_value = None

    result_fd = acquire_lock("test_lock_file")

    assert result_fd == mock_fd
    mock_open.assert_called_once_with(
        "test_lock_file", os.O_RDWR | os.O_CREAT | os.O_TRUNC
    )
    mock_flock.assert_called_once_with(mock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    mock_close.assert_not_called()
    mock_log.info.assert_not_called()


@patch("ublue_update.filelock.os.open")
@patch("ublue_update.filelock.fcntl.flock")
@patch("ublue_update.filelock.os.close")
@patch("ublue_update.filelock.time.sleep", return_value=None)
@patch("ublue_update.filelock.log")
def test_acquire_lock_timeout(mock_log, mock_sleep, mock_close, mock_flock, mock_open):
    mock_fd = 3
    mock_open.return_value = mock_fd
    mock_flock.side_effect = IOError

    result_fd = acquire_lock("test_lock_file")

    assert result_fd is None
    mock_open.assert_called_once_with(
        "test_lock_file", os.O_RDWR | os.O_CREAT | os.O_TRUNC
    )
    assert mock_flock.call_count >= 5
    mock_close.assert_called_once_with(mock_fd)
    mock_log.info.assert_called()


@patch("ublue_update.filelock.fcntl.flock")
@patch("ublue_update.filelock.os.close")
def test_release_lock(mock_close, mock_flock):
    mock_fd = 3

    result = release_lock(mock_fd)

    mock_flock.assert_called_once_with(mock_fd, fcntl.LOCK_UN)
    mock_close.assert_called_once_with(mock_fd)
    assert result is None

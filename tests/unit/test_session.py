import sys
import os
from unittest.mock import patch, MagicMock

# Add the src directory to the sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from ublue_update.session import get_active_users, run_uid

busctl_json_output = b"""{"type":"a(uso)","data":[[[1000,"user","/org/freedesktop/login1/user/_1000"]]]}"""


@patch("ublue_update.session.subprocess.run")
def test_get_active_users(mock_run):
    mock_run.side_effect = [
        MagicMock(stdout=busctl_json_output),
    ]
    assert get_active_users() == [
        [
            1000,
            "user",
            "/org/freedesktop/login1/user/_1000",
        ]
    ]
    mock_run.assert_any_call(
        [
            "/usr/bin/busctl",
            "--system",
            "-j",
            "call",
            "org.freedesktop.login1",
            "/org/freedesktop/login1",
            "org.freedesktop.login1.Manager",
            "ListUsers",
        ],
        capture_output=True,
    )


@patch("ublue_update.session.subprocess.run")
def test_run_uid(mock_run):
    mock_run.side_effect = [
        MagicMock(stdout=b"hi"),
    ]
    assert run_uid(0, ["echo", "hi"]).stdout.decode("utf-8") == "hi"
    mock_run.assert_called_once_with(
        [
            "/usr/bin/systemd-run",
            "--user",
            "--machine",
            "0@",
            "--pipe",
            "--quiet",
            "echo",
            "hi",
        ],
        capture_output=True,
    )

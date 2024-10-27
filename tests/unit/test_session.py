import sys
import os
from unittest.mock import patch, MagicMock, mock_open

# Add the src directory to the sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from ublue_update.session import get_active_users

busctl_json_output = b"""
{'type': 'a(uso)', 'data': [[[1000, 'user', '/org/freedesktop/login1/user/_1000']]]
"""


@patch("ublue_update.session.subprocess.run")
def test_get_active_sessions(mock_run):
    mock_run.side_effect = [
        MagicMock(stdout=busctl_json_output),
    ]
    assert get_active_sessions() == [
        [
            [
                "1000",
                "user",
                "/org/freedesktop/login1/user/_1000",
            ]
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

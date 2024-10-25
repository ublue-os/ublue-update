import sys
import os
from unittest.mock import patch, MagicMock, mock_open

# Add the src directory to the sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from ublue_update.session import get_active_sessions

loginctl_json_output = b"""
[
        {
                "session" : "3",
                "uid" : 1001,
                "user" : "test",
                "seat" : null,
                "leader" : 6205,
                "class" : "manager",
                "tty" : null,
                "state": "active",
                "idle" : false,
                "since" : null
        },
        {
                "session" : "c1",
                "uid" : 1001,
                "user" : "test",
                "seat" : null,
                "leader" : 6230,
                "class" : "manager",
                "tty" : null,
                "state": "inactive",
                "idle" : false,
                "since" : null
        }
]
"""


@patch("ublue_update.session.subprocess.run")
def test_get_active_sessions(mock_run):
    mock_run.side_effect = [
        MagicMock(stdout=loginctl_json_output),
    ]
    assert get_active_sessions() == [
        {
            "session": "3",
            "uid": 1001,
            "user": "test",
            "seat": None,
            "leader": 6205,
            "class": "manager",
            "tty": None,
            "state": "active",
            "idle": False,
            "since": None,
        }
    ]
    mock_run.assert_any_call(
        ["/usr/bin/loginctl", "list-sessions", "-j"], capture_output=True
    )

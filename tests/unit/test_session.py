import sys
import os
from unittest.mock import patch, MagicMock, mock_open

# Add the src directory to the sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from ublue_update.session import get_active_sessions, get_xdg_runtime_dir

loginctl_output = b"""
UID=1001
GID=1001
Name=test
Timestamp=Thu 2024-08-15 18:18:08 UTC
TimestampMonotonic=293807858
RuntimePath=/run/user/1001
Service=user@1001.service
Slice=user-1001.slice
Display=c3
State=active
Sessions=c4 c3 c1 3
IdleHint=no
IdleSinceHint=0
IdleSinceHintMonotonic=0
Linger=yes
"""

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
                "idle" : false,
                "since" : null
        }
]
"""

session_info = [
    b"""
Id=3
User=1001
Name=test
Timestamp=Thu 2024-08-15 18:18:08 UTC
TimestampMonotonic=293993628
VTNr=0
Remote=no
Service=systemd-user
Leader=6205
Audit=3
Type=wayland
Class=manager
Active=yes
State=active
IdleHint=no
IdleSinceHint=0
IdleSinceHintMonotonic=0
LockedHint=no
""",
    b"""
Id=c1
User=1001
Name=test
Timestamp=Thu 2024-08-15 18:18:09 UTC
TimestampMonotonic=295100128
VTNr=0
Remote=no
Service=systemd-user
Leader=6230
Audit=3
Type=unspecified
Class=manager
Active=yes
State=active
IdleHint=no
IdleSinceHint=0
IdleSinceHintMonotonic=0
LockedHint=no
""",
]


@patch("ublue_update.session.subprocess.run")
def test_get_xdg_runtime_dir(mock_run):
    mock_run.return_value = MagicMock(stdout=loginctl_output)
    assert get_xdg_runtime_dir(1001) == "/run/user/1001"
    mock_run.assert_called_once_with(
        ["/usr/bin/loginctl", "show-user", "1001"], capture_output=True
    )


@patch("ublue_update.session.subprocess.run")
def test_get_active_sessions(mock_run):
    mock_session1 = MagicMock(stdout=session_info[0])
    mock_session2 = MagicMock(stdout=session_info[1])
    mock_session1.returncode = 0
    mock_session2.returncode = 0
    mock_run.side_effect = [
        MagicMock(stdout=loginctl_json_output),
        mock_session1,
        mock_session2,
    ]
    assert get_active_sessions() == [
        {
            "": "",
            "Id": "3",
            "User": "1001",
            "Name": "test",
            "Timestamp": "Thu 2024-08-15 18:18:08 UTC",
            "TimestampMonotonic": "293993628",
            "VTNr": "0",
            "Remote": "no",
            "Service": "systemd-user",
            "Leader": "6205",
            "Audit": "3",
            "Type": "wayland",
            "Class": "manager",
            "Active": "yes",
            "State": "active",
            "IdleHint": "no",
            "IdleSinceHint": "0",
            "IdleSinceHintMonotonic": "0",
            "LockedHint": "no",
        }
    ]
    mock_run.assert_any_call(
        ["/usr/bin/loginctl", "list-sessions", "--output=json"], capture_output=True
    )
    mock_run.assert_any_call(
        ["/usr/bin/loginctl", "show-session", "3"], capture_output=True
    )
    mock_run.assert_any_call(
        ["/usr/bin/loginctl", "show-session", "c1"], capture_output=True
    )

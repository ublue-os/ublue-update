import subprocess
import json


def get_active_sessions():
    out = subprocess.run(
        ["/usr/bin/loginctl", "list-sessions", "--output=json"],
        capture_output=True,
    )
    sessions = json.loads(out.stdout.decode("utf-8"))
    active_sessions = []
    for session in sessions:
        if session.get("state") == "active":
            active_sessions.append(session)
    return active_sessions

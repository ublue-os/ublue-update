import subprocess
import json


def get_xdg_runtime_dir(uid):
    out = subprocess.run(
        ["/usr/bin/loginctl", "show-user", f"{uid}"],
        capture_output=True,
    )
    loginctl_output = {
        line.split("=")[0]: line.split("=")[-1]
        for line in out.stdout.decode("utf-8").splitlines()
    }
    return loginctl_output["RuntimePath"]


def get_active_sessions():
    out = subprocess.run(
        ["/usr/bin/loginctl", "list-sessions", "--output=json"],
        capture_output=True,
    )
    sessions = json.loads(out.stdout.decode("utf-8"))
    session_properties = []
    active_sessions = []
    for session in sessions:
        args = [
            "/usr/bin/loginctl",
            "show-session",
            session["session"],
        ]
        out = subprocess.run(args, capture_output=True)
        loginctl_output = {
            line.split("=")[0]: line.split("=")[-1]
            for line in out.stdout.decode("utf-8").splitlines()
        }
        session_properties.append(loginctl_output)
    for session_info in session_properties:
        graphical = session_info["Type"] == "x11" or session_info["Type"] == "wayland"
        if graphical and session_info["Active"] == "yes":
            active_sessions.append(session_info)
    return active_sessions

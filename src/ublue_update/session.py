import subprocess
import json


def get_active_users():
    out = subprocess.run(
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
    # https://www.freedesktop.org/software/systemd/man/latest/org.freedesktop.login1.html
    # ListUsers() returns an array of all currently logged in users. The structures in the array consist of the following fields: user id, user name, user object path.
    users = json.loads(out.stdout.decode("utf-8"))
    # sample output: {'type': 'a(uso)', 'data': [[[1000, 'user', '/org/freedesktop/login1/user/_1000']]]
    return users["data"][0]

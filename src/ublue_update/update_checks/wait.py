from json import loads
from subprocess import PIPE, run
from time import sleep


def transaction():
    """Pull deployment status via rpm-ostree"""
    rpm_ostree_status = ["rpm-ostree", "status",  "--json"]
    status = run(rpm_ostree_status, stdout=PIPE)
    """Parse transaction state"""
    return loads(status.stdout)["transaction"]


def transaction_wait():
    while transaction() is not None:
        sleep(1)

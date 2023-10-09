from json import loads
from json.decoder import JSONDecodeError
from subprocess import PIPE, run
from time import sleep
from logging import getLogger

"""Setup logging"""
log = getLogger(__name__)


def transaction():
    try:
        """Pull deployment status via rpm-ostree"""
        rpm_ostree_status = ["/usr/bin/rpm-ostree", "status", "--json"]
        status = run(rpm_ostree_status, stdout=PIPE)
        """Parse transaction state"""
        return loads(status.stdout)["transaction"]
    except (JSONDecodeError, KeyError):
        log.error(
            "can't get transaction, system not managed with rpm-ostree container native"
        )
        return None


def transaction_wait():
    while transaction() is not None:
        sleep(1)

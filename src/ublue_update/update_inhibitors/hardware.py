import psutil
import subprocess
from logging import getLogger
from ublue_update.config import cfg

"""Setup logging"""
log = getLogger(__name__)


def check_network_status() -> dict:
    network_status = psutil.net_if_stats()
    # check each network interface
    network_up = False
    for key in network_status.keys():
        if key != "lo":
            if network_status[key][0]:
                network_up = True
                break
    return {"passed": network_up, "message": "Network not enabled"}


def check_network_not_metered() -> dict:
    if not cfg.network_not_metered:
        return {
            "passed": True,
            "message": "Network metering status is ignored",
        }
    # Use busctl CLI to query the NetworkManager via D-Bus for
    # the current metering status of the connection.
    # The output on stdout will be "<datatype> <value>".
    metered_status = subprocess.run(
        [
            "busctl",
            "get-property",
            "org.freedesktop.NetworkManager",
            "/org/freedesktop/NetworkManager",
            "org.freedesktop.NetworkManager",
            "Metered",
        ],
        capture_output=True,
        check=True,
        text=True,
    ).stdout
    # The possible values of "Metered" are documented here:
    # https://networkmanager.dev/docs/api/latest/nm-dbus-types.html#NMMetered
    #
    #     NM_METERED_UNKNOWN   = 0 # The metered status is unknown
    #     NM_METERED_YES       = 1 # Metered, the value was explicitly configured
    #     NM_METERED_NO        = 2 # Not metered, the value was explicitly configured
    #     NM_METERED_GUESS_YES = 3 # Metered, the value was guessed
    #     NM_METERED_GUESS_NO  = 4 # Not metered, the value was guessed
    #
    is_network_metered = metered_status.strip() in ["u 1", "u 3"]
    return {
        "passed": not is_network_metered,
        "message": "Network is metered",
    }


def check_battery_status() -> dict:
    if cfg.min_battery_percent:
        battery_status = psutil.sensors_battery()
        # null safety on the battery variable, it returns "None"
        # when the system doesn't have a battery
        battery_pass: bool = True
        if battery_status is not None:
            battery_pass = (
                battery_status.percent >= cfg.min_battery_percent
                or battery_status.power_plugged
            )
        return {
            "passed": battery_pass,
            "message": f"Battery less than {cfg.min_battery_percent}%",
        }
    else:
        return {
            "passed": True,
            "message": "Battery status is ignored",
        }


def check_cpu_load() -> dict:
    cores = psutil.cpu_count()
    if cfg.max_cpu_load_percent and cores is not None:
        # get load average percentage in last 5 minutes:
        # https://psutil.readthedocs.io/en/latest/index.html?highlight=getloadavg
        cpu_load_percent = psutil.getloadavg()[1] / cores * 100
        return {
            "passed": cpu_load_percent < cfg.max_cpu_load_percent,
            "message": f"CPU load is above {cfg.max_cpu_load_percent}%",
        }
    else:
        return {
            "passed": True,
            "message": "CPU load is ignored",
        }


def check_mem_percentage() -> dict:
    if cfg.max_mem_percent:
        mem = psutil.virtual_memory()
        return {
            "passed": mem.percent < cfg.max_mem_percent,
            "message": f"Memory usage is above {cfg.max_mem_percent}%",
        }
    else:
        return {
            "passed": True,
            "message": "Memory usage is ignored",
        }


def check_hardware_inhibitors() -> tuple[bool, list]:
    hardware_inhibitors = [
        check_network_status(),
        check_network_not_metered(),
        check_battery_status(),
        check_cpu_load(),
        check_mem_percentage(),
    ]

    failures = []
    hardware_checks_failed = False
    for inhibitor_result in hardware_inhibitors:
        if not inhibitor_result["passed"]:
            hardware_checks_failed = True
            failures.append(inhibitor_result["message"])
    if not hardware_checks_failed:
        log.info("System passed hardware checks")
    return hardware_checks_failed, failures

import psutil
from logging import getLogger
from ublue_update.config import load_value

"""Setup logging"""
log = getLogger(__name__)

min_battery_percent: float = load_value("checks", "min_battery_percent")
max_cpu_load_percent: float = load_value("checks", "max_cpu_load_percent")
max_mem_percent: float = load_value("checks", "max_mem_percent")


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


def check_battery_status() -> dict:
    battery_status = psutil.sensors_battery()
    # null safety on the battery variable, it returns "None"
    # when the system doesn't have a battery
    battery_pass: bool = True
    if battery_status is not None:
        battery_pass = (
            battery_status.percent >= min_battery_percent or battery_status.power_plugged
        )
    return {
        "passed": battery_pass,
        "message": f"Battery less than {min_battery_percent}%",
    }


def check_cpu_load() -> dict:
    # get load average percentage in last 5 minutes:
    # https://psutil.readthedocs.io/en/latest/index.html?highlight=getloadavg
    cpu_load_percent = psutil.getloadavg()[1] / psutil.cpu_count() * 100
    return {
        "passed": cpu_load_percent < max_cpu_load_percent,
        "message": f"CPU load is above {max_cpu_load_percent}%",
    }


def check_mem_percentage() -> dict:
    mem = psutil.virtual_memory()
    return {
        "passed": mem.percent < max_mem_percent,
        "message": f"Memory usage is above {max_mem_percent}%",
    }


def check_hardware_inhibitors() -> bool:

    hardware_inhibitors = [
        check_network_status(),
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

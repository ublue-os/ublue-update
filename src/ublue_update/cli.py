import psutil

import os
import subprocess
import logging
import tomllib
import argparse
from ublue_update.notification_manager import NotificationManager


def check_cpu_load():
    # get load average percentage in last 5 minutes:
    # https://psutil.readthedocs.io/en/latest/index.html?highlight=getloadavg
    cpu_load = psutil.getloadavg()[1] / psutil.cpu_count() * 100
    return {
        "passed": cpu_load < max_cpu_load,
        "message": f"CPU load is above {max_cpu_load}%",
    }


def check_network_status():
    network_status = psutil.net_if_stats()
    # check each network interface
    network_up = False
    for key in network_status.keys():
        if key != "lo":
            if network_status[key][0]:
                network_up = True
                break
    return {"passed": network_up, "message": "Network not enabled"}


def check_battery_status():
    battery_status = psutil.sensors_battery()
    # null safety on the battery variable, it returns "None"
    # when the system doesn't have a battery
    battery_pass = True
    if battery_status is not None:
        battery_pass = (
            battery_status.percent > min_battery_percent or battery_status.power_plugged
        )
    return {
        "passed": battery_pass,
        "message": f"Battery less than {min_battery_percent}%",
    }


def check_inhibitors():

    update_inhibitors = [
        check_network_status(),
        check_battery_status(),
        check_cpu_load(),
    ]

    failures = []
    update_checks_failed = False
    for inhibitor_result in update_inhibitors:
        if not inhibitor_result["passed"]:
            update_checks_failed = True
            failures.append(inhibitor_result["message"])

    # log the failed update
    if update_checks_failed:
        # notify systemd that the checks have failed,
        # systemd will try to rerun the unit
        exception_log = "\n - ".join(failures)
        raise Exception(f"update failed to pass checks: \n - {exception_log}")


def load_config():
    # load config values
    config_paths = [
        os.path.expanduser("~/.config/ublue-update/ublue-update.toml"),
        "/etc/ublue-update/ublue-update.toml",
        "/usr/etc/ublue-update/ublue-update.toml",
    ]

    # search for the right config
    config_path = ""
    fallback_config_path = ""
    for path in config_paths:
        if os.path.isfile(path):
            if config_path == "":
                config_path = path
            fallback_config_path = path
            break

    fallback_config = tomllib.load(open(fallback_config_path, "rb"))
    config = tomllib.load(open(config_path, "rb"))
    return config, fallback_config


def load_value(key, value):
    fallback = fallback_config[key][value]
    if key in config.keys():
        return config[key].get(value, fallback)
    return fallback


def run_updates():
    root_dir = "/etc/ublue-update.d/"

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            full_path = root_dir + "/" + str(file)

            executable = os.access(full_path, os.X_OK)
            if executable:
                out = subprocess.run(
                    [full_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )

                if out.returncode != 0:
                    log.info(f"{full_path} returned error code: {out.returncode}")
                    log.info("Program output: \n {out.stdout}")
                    if dbus_notify:
                        notification_manager.notification(
                            "System Updater",
                            f"Error in update script: {file}, check logs for more info",
                        ).show(5)
            else:
                log.info(f"could not execute file {full_path}")


config, fallback_config = load_config()

dbus_notify = load_value("notify", "dbus_notify")
min_battery_percent = load_value("checks", "battery_percent")
max_cpu_load = load_value("checks", "cpu_load")

# setup logging
logging.basicConfig(
    format="[%(asctime)s] %(name)s:%(levelname)s | %(message)s",
    level=os.getenv("UBLUE_LOG", default=logging.INFO),
)
log = logging.getLogger(__name__)

notification_manager = NotificationManager("Universal Blue Updater")

#if dbus_notify:

def main():

    # setup argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="force manual update, skipping update checks",
    )
    parser.add_argument(
        "-c", "--check", action="store_true", help="run update checks and exit"
    )
    args = parser.parse_args()

    if not args.force:
        check_inhibitors()

    # system checks passed
    log.info("System passed all update checks")
    if dbus_notify:
        notification_manager.notification(
            "System Updater",
            "System passed checks, updating ...",
        ).show(5)

    if args.check:
        exit(0)

    run_updates()
    if dbus_notify:
        notification_manager.notification(
            "System Updater",
            "System update complete, reboot for changes to take effect",
        ).show(5)
    log.info("System update complete")

import tomllib
import os
from typing import List, Optional
from logging import getLogger

"""Setup logging"""
log = getLogger(__name__)


def find_default_config_file():
    # load config values
    config_paths = [
        "/etc/ublue-update/ublue-update.toml",
        "/usr/etc/ublue-update/ublue-update.toml",
    ]

    # search for the right config
    # first config file that is found wins
    for path in config_paths:
        if os.path.isfile(path):
            return path

    return None


def load_value(dct, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct


class Config:
    dbus_notify: bool
    network_not_metered: Optional[bool]
    min_battery_percent: Optional[float]
    max_cpu_load_percent: Optional[float]
    max_mem_percent: Optional[float]
    custom_check_scripts: List[dict]

    def load_config(self, path=None):
        config_path = path or find_default_config_file()
        config = tomllib.load(open(config_path, "rb"))
        log.debug(f"Configuration loaded from {os.path.abspath(config_path)}")
        self.load_values(config)

    def load_values(self, config):
        self.dbus_notify = load_value(config, "notify", "dbus_notify") or False
        self.network_not_metered = load_value(config, "checks", "network_not_metered")
        self.min_battery_percent = load_value(config, "checks", "min_battery_percent")
        self.max_cpu_load_percent = load_value(config, "checks", "max_cpu_load_percent")
        self.max_mem_percent = load_value(config, "checks", "max_mem_percent")
        self.custom_check_scripts = load_value(config, "checks", "scripts") or []


cfg = Config()

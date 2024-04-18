import tomllib
import os


def load_config():
    # load config values
    config_paths = [
        "/etc/ublue-update/ublue-update.toml",
        "/usr/etc/ublue-update/ublue-update.toml",
    ]

    # search for the right config
    # first config file that is found wins
    for path in config_paths:
        if os.path.isfile(path):
            return tomllib.load(open(path, "rb"))

    return config


def safe_get_nested(dct, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct


def load_value(*keys):
    return safe_get_nested(config, *keys)


config = load_config()

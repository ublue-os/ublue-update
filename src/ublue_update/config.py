import tomllib
import os


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


config, fallback_config = load_config()

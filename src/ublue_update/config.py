import tomllib
import os


def load_config():
    # load config values
    config_paths = [
        "/etc/ublue-update/ublue-update.toml",
        "/usr/etc/ublue-update/ublue-update.toml",
    ]

    # search for the right config
    # BUG: config_path and fallback_config_path always have the same value
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


def safe_get_nested(dct, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct


def load_value(*keys):
    return safe_get_nested(config, *keys) or safe_get_nested(fallback_config, *keys)


config, fallback_config = load_config()

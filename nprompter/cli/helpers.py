import importlib
import os

import tomli

import nprompter
import nprompter.cli.defaults


def get_config(configuration_file):
    config_dict = tomli.loads(importlib.resources.read_text(nprompter.web, "config.toml"))
    if os.path.exists(configuration_file or nprompter.cli.defaults.DEFAULT_APPEARANCE_CONFIG_PATH):
        with open(configuration_file, "rb") as readable:
            user_defined_config = tomli.load(readable)
            config_dict.update(user_defined_config)
    return config_dict

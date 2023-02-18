import importlib
import importlib.resources
import os

import tomli

import nprompter
import nprompter.cli.defaults
import nprompter.web


def recursive_update(base, new):
    # Recursively update a dictionary with another dictionary
    for k, v in new.items():
        if isinstance(v, dict):
            base[k] = recursive_update(base.get(k, {}), v)
        else:
            base[k] = v
    return base


def get_config(configuration_file):
    base_config = tomli.loads(importlib.resources.read_text(nprompter.web, nprompter.cli.defaults.DEFAULT_CONFIG_PATH))
    configuration_file = configuration_file or nprompter.cli.defaults.DEFAULT_CONFIG_PATH
    if os.path.exists(configuration_file):
        with open(configuration_file, "rb") as readable:
            user_defined_config = tomli.load(readable)
        base_config = recursive_update(base_config, user_defined_config)
    return base_config

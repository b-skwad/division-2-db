"""Utilities and primitives for the `division-server` CLI command."""

import os

from django.core.management.utils import get_random_secret_key
from jinja2 import BaseLoader, Environment

from division.core.runner import run_app

# Default file location for the generated config emitted by `init`
DIVISION_ROOT = os.getenv("DIVISION_ROOT", os.path.expanduser("~/.Division 2 DB"))
DEFAULT_CONFIG_PATH = os.path.join(DIVISION_ROOT, "division_config.py")

# Default settings to use when building the config
DEFAULT_SETTINGS = "division.core.settings"

# Name of the environment variable used to specify path of config
SETTINGS_ENVVAR = "DIVISION_CONFIG"

# Base directory for this module
BASE_DIR = os.path.dirname(__file__)

# File path of template used to generate config emitted by `init`
CONFIG_TEMPLATE = os.path.join(BASE_DIR, "templates/division_config.py.j2")

DESCRIPTION = """
division_build server management utility.

Type '%(prog)s help' to display a list of included sub-commands.

Type '%(prog)s init' to generate a new configuration.
"""


def main():
    """
    The main server CLI command that replaces `manage.py` and allows a configuration file to be passed in.

    How this works:

    - Process CLI args
    - Load default settings
    - Read config file from path
    - Overlay config settings on top of default settings
    - Overlay special/conditional settings (see `_configure_settings`)
    """
    run_app(
        project="division",
        description=DESCRIPTION,
        default_config_path=DEFAULT_CONFIG_PATH,
        default_settings=DEFAULT_SETTINGS,
        settings_initializer=generate_settings,
        settings_envvar=SETTINGS_ENVVAR,
        initializer=_configure_settings,  # Called after defaults
    )


def generate_settings(config_template=CONFIG_TEMPLATE, **kwargs):
    """
    Settings generator.

    This command is ran when `default_config_path` doesn't exist, or `init` is
    ran and returns a string representing the default data to put into the
    settings file.
    """
    secret_key = get_random_secret_key()

    with open(config_template) as fh:
        environment = Environment(loader=BaseLoader, keep_trailing_newline=True)
        config = environment.from_string(fh.read())

    return config.render(secret_key=secret_key)


def _configure_settings(config):
    """
    Callback for processing conditional or special purpose settings.

    Any specially prepared settings will be handled here, such as loading
    plugins, enabling social auth, etc.

    This is intended to be called by `run_app` and should not be invoked
    directly.

    :param config:
        A dictionary of `config_path`, `project`, `settings`

    Example::

        {
            'project': 'Division 2 DB',
            'config_path': '/path/to/division_config.py',
            'settings': <LazySettings "division_config">
        }
    """
    settings = config["settings"]

    # Include the config path to the settings to align with builtin
    # `settings.SETTINGS_MODULE`. Useful for debugging correct config path.
    settings.SETTINGS_PATH = config["config_path"]

    #
    # Storage directories
    #
    if not os.path.exists(settings.STATIC_ROOT):
        os.makedirs(settings.STATIC_ROOT)


if __name__ == "__main__":
    main()

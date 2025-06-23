"""This script provides functions to initialize the module logger from a config yaml."""

from __future__ import annotations  # Compatibility of "|" Unions in python 3.9

import atexit
import logging
import logging.config
import logging.handlers
import pathlib
import sys

import yaml

# Check if the Python version is 3.9
if sys.version_info.major == 3 and sys.version_info.minor == 9:
    # pylint: disable-next=import-error
    from overrides import override
else:
    # pylint: disable-next=no-name-in-module
    from typing import override


def setup_logging_3_11() -> None:
    """Setup logger for python 3.9 through 3.11."""
    config_file = pathlib.Path.cwd() / "log_config_3_11.yaml"
    with open(config_file, encoding="utf-8") as f_in:
        config = yaml.load(f_in, yaml.SafeLoader)

    logging.config.dictConfig(config)


def setup_logging() -> None:
    """Setup logger for python 3.12 and newer."""
    config_file = pathlib.Path.cwd() / "log_config.yaml"
    with open(config_file, encoding="utf-8") as f_in:
        config = yaml.load(f_in, yaml.SafeLoader)

    logging.config.dictConfig(config)
    # pylint: disable-next=no-member
    queue_handler: logging.Handler | None = logging.getHandlerByName("queue_handler")
    if isinstance(queue_handler, logging.handlers.QueueHandler):
        assert queue_handler.listener is not None
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


# pylint: disable-next=too-few-public-methods
class NonErrorFilter(logging.Filter):
    """Defines a filter level for logs below logging.ERROR."""

    @override
    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        return record.levelno <= logging.INFO

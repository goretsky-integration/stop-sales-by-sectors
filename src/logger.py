import json
import logging.config
import pathlib

import config

__all__ = ('create_logger', 'load_logging_config', 'setup_logging')


def create_logger(name: str) -> logging.Logger:
    """Create logger which doesn't propagate messages to the root logger."""
    logger = logging.getLogger(name)
    logger.propagate = False
    return logger


def load_logging_config(
        file_path: pathlib.Path = config.LOGGING_CONFIG_FILE_PATH,
) -> dict:
    logging_config = file_path.read_text(encoding='utf-8')
    return json.loads(logging_config)


def setup_logging():
    logging_config = load_logging_config()
    logging.config.dictConfig(logging_config)

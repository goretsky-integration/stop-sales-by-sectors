import pathlib

from pydantic import TypeAdapter

import config
from logger import create_logger
from models import AccountUnits

__all__ = ('load_units',)

logger = create_logger('units')


def load_units(
        file_path: pathlib.Path = config.ACCOUNTS_UNITS_FILE_PATH,
) -> list[AccountUnits]:
    type_adapter = TypeAdapter(list[AccountUnits])
    try:
        config_json = file_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        logger.error('File with accounts units not found')
        raise
    return type_adapter.validate_json(config_json)

import pathlib
import tomllib
from dataclasses import dataclass
from zoneinfo import ZoneInfo

from enums import CountryCode

__all__ = (
    'Config',
    'get_config',
    'SOURCE_DIR',
    'CONFIG_FILE_PATH',
    'ACCOUNTS_UNITS_FILE_PATH',
    'LOGGING_CONFIG_FILE_PATH',
)

SOURCE_DIR = pathlib.Path(__file__).parent
CONFIG_FILE_PATH = SOURCE_DIR.parent / "config.toml"
ACCOUNTS_UNITS_FILE_PATH = SOURCE_DIR.parent / 'accounts_units.json'
LOGGING_CONFIG_FILE_PATH = SOURCE_DIR.parent / 'logging_config.json'


@dataclass(frozen=True, slots=True)
class Config:
    app_name: str
    timezone: ZoneInfo
    country_code: CountryCode
    units_storage_base_url: str
    auth_credentials_storage_base_url: str
    message_queue_url: str
    redis_url: str


def get_config() -> Config:
    config_text = CONFIG_FILE_PATH.read_text(encoding='utf-8')
    config = tomllib.loads(config_text)

    return Config(
        app_name=config['app']['name'],
        timezone=ZoneInfo(config['app']['timezone']),
        country_code=CountryCode(config['app']['country_code']),
        units_storage_base_url=config['units_storage']['base_url'],
        auth_credentials_storage_base_url=(
            config['auth_credentials_storage']['base_url']
        ),
        message_queue_url=config['message_queue']['url'],
        redis_url=config['redis']['url'],
    )

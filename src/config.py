import pathlib
import tomllib
from dataclasses import dataclass
from zoneinfo import ZoneInfo

from enums import CountryCode

__all__ = (
    'Config',
    'get_config',
)

CONFIG_FILE_PATH = pathlib.Path(__file__).parent.parent / "config.toml"


@dataclass(frozen=True, slots=True)
class Config:
    app_name: str
    timezone: ZoneInfo
    country_code: CountryCode
    units_storage_base_url: str


def get_config() -> Config:
    config_text = CONFIG_FILE_PATH.read_text(encoding='utf-8')
    config = tomllib.loads(config_text)

    return Config(
        app_name=config['app']['name'],
        timezone=ZoneInfo(config['app']['timezone']),
        country_code=CountryCode(config['app']['country_code']),
        units_storage_base_url=config['units_storage']['base_url'],
    )

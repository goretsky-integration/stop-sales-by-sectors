import httpx
from fast_depends import Depends

from config import Config, get_config
from connections.units_storage import UnitsStorageConnection
from context.units_storage import UnitsStorageContext
from new_types import UnitsStorageHttpClient

__all__ = (
    'get_units_storage_connection',
    'get_units_storage_http_client',
    'get_units_storage_context',
)


def get_units_storage_http_client(
        config: Config = Depends(get_config, use_cache=True),
) -> UnitsStorageHttpClient:
    with httpx.Client(base_url=config.units_storage_base_url) as http_client:
        yield UnitsStorageHttpClient(http_client)


def get_units_storage_connection(
        http_client: UnitsStorageHttpClient = Depends(
            get_units_storage_http_client,
            use_cache=False,
        ),
):
    return UnitsStorageConnection(http_client)


def get_units_storage_context(
        connection: UnitsStorageConnection = Depends(
            get_units_storage_connection,
            use_cache=False,
        ),
) -> UnitsStorageContext:
    return UnitsStorageContext(connection)

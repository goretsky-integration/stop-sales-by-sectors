from collections.abc import Generator

import httpx
from fast_depends import Depends

from config import Config, get_config
from connections.auth_credentials_storage import (
    AuthCredentialsStorageConnection,
)
from connections.dodo_is import DodoIsConnection
from connections.units_storage import UnitsStorageConnection
from context.auth_credentials_storage import AuthCredentialsStorageContext
from context.dodo_is import DodoIsContext
from context.units_storage import UnitsStorageContext
from new_types import (
    AuthCredentialsStorageHttpClient,
    DodoISHttpClient,
    UnitsStorageHttpClient,
)

__all__ = (
    'get_units_storage_connection',
    'get_units_storage_http_client',
    'get_units_storage_context',
    'get_dodo_is_http_client',
    'get_dodo_is_context',
    'get_dodo_is_connection',
    'get_auth_credentials_storage_context',
    'get_auth_credentials_storage_http_client',
    'get_auth_credentials_storage_connection',
)


def get_units_storage_http_client(
        config: Config = Depends(get_config, use_cache=True),
) -> Generator[UnitsStorageHttpClient, None, None]:
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


def get_dodo_is_http_client(
        config: Config = Depends(get_config, use_cache=True),
) -> Generator[DodoISHttpClient, None, None]:
    base_url = f'https://api.dodois.io/dodopizza/{config.country_code}/'
    with httpx.Client(base_url=base_url) as http_client:
        yield DodoISHttpClient(http_client)


def get_dodo_is_connection(
        http_client: DodoISHttpClient = Depends(
            get_dodo_is_http_client,
            use_cache=False,
        ),
) -> DodoIsConnection:
    return DodoIsConnection(http_client)


def get_dodo_is_context(
        connection: DodoIsConnection = Depends(
            get_dodo_is_connection,
            use_cache=False,
        ),
) -> DodoIsContext:
    return DodoIsContext(connection)


def get_auth_credentials_storage_http_client(
        config: Config = Depends(get_config, use_cache=True),
) -> Generator[AuthCredentialsStorageHttpClient, None, None]:
    base_url = config.auth_credentials_storage_base_url
    with httpx.Client(base_url=base_url) as http_client:
        yield AuthCredentialsStorageHttpClient(http_client)


def get_auth_credentials_storage_connection(
        http_client: AuthCredentialsStorageHttpClient = Depends(
            get_auth_credentials_storage_http_client,
            use_cache=False,
        ),
):
    return AuthCredentialsStorageConnection(http_client)


def get_auth_credentials_storage_context(
        connection: AuthCredentialsStorageConnection = Depends(
            get_auth_credentials_storage_connection,
            use_cache=False,
        ),
) -> AuthCredentialsStorageContext:
    return AuthCredentialsStorageContext(connection)

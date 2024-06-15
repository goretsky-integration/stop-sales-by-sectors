from collections.abc import AsyncGenerator

import httpx
from fast_depends import Depends
from faststream.rabbit import RabbitBroker

from config import Config, get_config
from connections.auth_credentials_storage import (
    AuthCredentialsStorageConnection,
)
from connections.dodo_is import DodoIsConnection
from connections.event_publisher import EventPublisher
from new_types import (
    AuthCredentialsStorageHttpClient,
    DodoISHttpClient,
)

__all__ = (
    'get_dodo_is_http_client',
    'get_dodo_is_connection',
    'get_auth_credentials_storage_http_client',
    'get_auth_credentials_storage_connection',
    'get_message_queue_broker',
    'get_event_publisher',
)


async def get_dodo_is_http_client(
        config: Config = Depends(get_config),
) -> AsyncGenerator[DodoISHttpClient, None]:
    base_url = f'https://api.dodois.io/dodopizza/{config.country_code}/'
    async with httpx.AsyncClient(
            base_url=base_url,
            timeout=60,
    ) as http_client:
        yield DodoISHttpClient(http_client)


def get_dodo_is_connection(
        http_client: DodoISHttpClient = Depends(get_dodo_is_http_client),
) -> DodoIsConnection:
    return DodoIsConnection(http_client)


async def get_auth_credentials_storage_http_client(
        config: Config = Depends(get_config),
) -> AsyncGenerator[AuthCredentialsStorageHttpClient, None]:
    base_url = config.auth_credentials_storage_base_url
    async with httpx.AsyncClient(base_url=base_url) as http_client:
        yield AuthCredentialsStorageHttpClient(http_client)


def get_auth_credentials_storage_connection(
        http_client: AuthCredentialsStorageHttpClient = Depends(
            get_auth_credentials_storage_http_client,
        ),
):
    return AuthCredentialsStorageConnection(http_client)


async def get_message_queue_broker(
        config: Config = Depends(get_config),
) -> AsyncGenerator[RabbitBroker, None]:
    async with RabbitBroker(config.message_queue_url) as broker:
        yield broker


def get_event_publisher(
        broker: RabbitBroker = Depends(get_message_queue_broker),
):
    return EventPublisher(broker)

import httpx

from logger import create_logger
from new_types import AuthCredentialsStorageHttpClient

__all__ = ('AuthCredentialsStorageConnection',)

logger = create_logger('auth_credentials')


class AuthCredentialsStorageConnection:

    def __init__(
            self,
            http_client: AuthCredentialsStorageHttpClient,
    ):
        self.__http_client = http_client

    async def get_tokens(self, account_name: str) -> httpx.Response:
        url = '/auth/token/'
        request_query_params = {'account_name': account_name}

        logger.debug(
            'Retrieving tokens for account',
            extra={'account_name': account_name},
        )
        response = await self.__http_client.get(
            url=url,
            params=request_query_params,
        )
        logger.debug(
            'Retrieved tokens for account',
            extra={
                'account_name': account_name,
                'status_code': response.status_code,
            },
        )

        return response

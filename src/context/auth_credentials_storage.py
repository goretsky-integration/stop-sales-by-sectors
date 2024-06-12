import asyncio

from connections.auth_credentials_storage import (
    AuthCredentialsStorageConnection,
)
from logger import create_logger
from models import AccountTokens
from parsers.auth_credentials import parse_account_tokens_response

__all__ = ('AuthCredentialsFetchUnitOfWork',)

logger = create_logger('auth_credentials')


class AuthCredentialsFetchUnitOfWork:

    def __init__(self, connection: AuthCredentialsStorageConnection):
        self.__connection = connection
        self.__account_names: list[str] = []

    def register_task(self, account_name: str) -> None:
        self.__account_names.append(account_name)

    async def _get_account_tokens(self, account_name: str) -> AccountTokens:
        response = await self.__connection.get_tokens(account_name)
        return parse_account_tokens_response(response)

    async def commit(self) -> list[AccountTokens]:
        tasks = [
            self._get_account_tokens(account_name)
            for account_name in self.__account_names
        ]
        responses: tuple[AccountTokens | Exception, ...] = (
            await asyncio.gather(*tasks, return_exceptions=True)
        )

        result = []
        for response in responses:
            if isinstance(response, Exception):
                logger.exception(
                    f'Failed to fetch account tokens',
                    exc_info=response,
                )
            else:
                result.append(response)
        return result

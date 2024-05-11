import httpx

from new_types import AuthCredentialsStorageHttpClient

__all__ = ('AuthCredentialsStorageConnection',)


class AuthCredentialsStorageConnection:

    def __init__(
            self,
            http_client: AuthCredentialsStorageHttpClient,
    ):
        self.__http_client = http_client

    def get_tokens(self, account_name: str) -> httpx.Response:
        url = '/auth/cookies/'
        request_query_params = {'account_name': account_name}
        response = self.__http_client.get(
            url=url,
            params=request_query_params,
        )
        return response

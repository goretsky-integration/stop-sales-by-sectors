import httpx

from new_types import UnitsStorageHttpClient

__all__ = ('UnitsStorageConnection',)


class UnitsStorageConnection:

    def __init__(self, http_client: UnitsStorageHttpClient):
        self.__http_client = http_client

    def get_units(self) -> httpx.Response:
        return self.__http_client.get('/units/')

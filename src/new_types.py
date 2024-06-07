from typing import NewType

import httpx

__all__ = (
    'AuthCredentialsStorageHttpClient',
    'DodoISHttpClient',
)

AuthCredentialsStorageHttpClient = (
    NewType('AuthCredentialsStorageHttpClient', httpx.AsyncClient)
)
DodoISHttpClient = NewType('DodoISHttpClient', httpx.AsyncClient)

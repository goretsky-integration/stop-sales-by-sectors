from typing import NewType

import httpx

__all__ = (
    'UnitsStorageHttpClient',
    'AuthCredentialsStorageHttpClient',
    'DodoISHttpClient',
)

UnitsStorageHttpClient = NewType('UnitsStorageHttpClient', httpx.Client)
AuthCredentialsStorageHttpClient = (
    NewType('AuthCredentialsStorageHttpClient', httpx.Client)
)
DodoISHttpClient = NewType('DodoISHttpClient', httpx.Client)

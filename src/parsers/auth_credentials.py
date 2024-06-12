import httpx

from logger import create_logger
from models import AccountTokens

__all__ = ('parse_account_tokens_response',)

logger = create_logger('parser')


def parse_account_tokens_response(response: httpx.Response) -> AccountTokens:
    response_data = response.json()
    return AccountTokens.model_validate(response_data)

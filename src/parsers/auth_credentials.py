import json

import httpx
from pydantic import ValidationError

from logger import create_logger
from models import AccountTokens

__all__ = ('parse_account_tokens_response',)

logger = create_logger('parser')


def parse_account_tokens_response(response: httpx.Response) -> AccountTokens:
    """Parse the response from the account tokens response."""
    logger.info(
        'Parsing account tokens response',
        extra={'response_body': response.text}
    )
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        logger.error(
            'Failed to parse response data as JSON',
            extra={'response_body': response.text},
        )
        raise

    try:
        return AccountTokens.model_validate(response_data)
    except ValidationError:
        logger.error(
            'Failed to validate account tokens',
            extra={'response_body': response_data},
        )
        raise

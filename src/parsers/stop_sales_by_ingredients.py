import json

import httpx
from pydantic import TypeAdapter, ValidationError

from logger import create_logger
from models import StopSaleByIngredient

__all__ = ('parse_stop_sales_by_ingredients_response',)

logger = create_logger('parser')


def parse_stop_sales_by_ingredients_response(
        response: httpx.Response,
) -> list[StopSaleByIngredient]:
    logger.debug('Parsing stop sales by ingredients response')
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        logger.error(
            'Failed to parse response JSON',
            extra={'body': response.text}
        )
        raise

    type_adapter = TypeAdapter(list[StopSaleByIngredient])

    try:
        return type_adapter.validate_python(
            response_data['stopSalesByIngredients'],
        )
    except ValidationError:
        logger.error(
            'Failed to parse stop sales by ingredients [pydantic]',
            extra={'body': response.text}
        )
        raise

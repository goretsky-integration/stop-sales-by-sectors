import datetime
from collections.abc import Iterable
from uuid import UUID

import httpx

from logger import create_logger
from new_types import DodoISHttpClient

__all__ = ('build_request_query_params', 'DodoIsConnection')

logger = create_logger('dodo_is_api')


def build_request_query_params(
        *,
        unit_uuids: Iterable[UUID],
        from_date: datetime.datetime,
        to_date: datetime.datetime,
) -> dict[str, str]:
    return {
        'units': ','.join(unit_uuid.hex for unit_uuid in unit_uuids),
        'from': f'{from_date:%Y-%m-%dT%H:%M:%S}',
        'to': f'{to_date:%Y-%m-%dT%H:%M:%S}',
    }


class DodoIsConnection:

    def __init__(self, http_client: DodoISHttpClient):
        self.__http_client = http_client

    async def get_stop_sales_by_ingredients(
            self,
            *,
            unit_uuids: Iterable[UUID],
            from_date: datetime.datetime,
            to_date: datetime.datetime,
            access_token: str,
    ) -> httpx.Response:
        url = '/production/stop-sales-ingredients'
        query_params = build_request_query_params(
            unit_uuids=unit_uuids,
            from_date=from_date,
            to_date=to_date,
        )
        headers = {'Authorization': f'Bearer {access_token}'}

        logger.debug(
            'Retrieving stop sales by ingredients from Dodo IS',
            extra={'query_params': query_params},
        )
        response = await self.__http_client.get(
            url=url,
            params=query_params,
            headers=headers,
        )

        logger.debug(
            'Retrieved stop sales by ingredients from Dodo IS',
            extra={'status_code': response.status_code},
        )

        return response

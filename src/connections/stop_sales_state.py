from collections.abc import Iterable
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import redis.asyncio as redis

from models import StopSaleByIngredient

__all__ = ('compute_state_reset_time', 'StopSalesStateManager')


def compute_state_reset_time(timezone: ZoneInfo):
    tomorrow_this_moment = datetime.now(timezone) + timedelta(days=1)
    return tomorrow_this_moment.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )


class StopSalesStateManager:
    key = 'stop-sales-by-ingredients'

    def __init__(self, redis_client: redis.Redis, timezone: ZoneInfo):
        self.__redis_client = redis_client
        self.__timezone = timezone

    async def filter(self, stop_sales: Iterable[StopSaleByIngredient]):
        """Filter out stop sales that are already in the state."""
        result: list[StopSaleByIngredient] = []

        for stop_sale in stop_sales:
            is_exist = await self.__redis_client.sismember(
                self.key,
                stop_sale.id.hex,
            )

            if not is_exist:
                result.append(stop_sale)

        return result

    async def save(self, stop_sales: Iterable[StopSaleByIngredient]) -> None:
        """Save stop sales to the state."""
        reset_time = compute_state_reset_time(self.__timezone)
        stop_sale_ids = [stop_sale.id.hex for stop_sale in stop_sales]
        print(stop_sale_ids)

        await self.__redis_client.sadd(self.key, *stop_sale_ids)
        await self.__redis_client.expireat(self.key, reset_time, nx=True)

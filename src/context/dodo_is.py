import asyncio
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias
from uuid import UUID

from pydantic import SecretStr

from connections.dodo_is import DodoIsConnection
from logger import create_logger
from models import StopSaleByIngredient
from more_itertools import batched
from parsers.stop_sales_by_ingredients import (
    parse_stop_sales_by_ingredients_response,
)

__all__ = ('StopSalesFetcher',)

logger = create_logger('dodo_is_api')

AccessTokenAndUnitUuids: TypeAlias = tuple[SecretStr, Iterable[UUID]]


@dataclass(frozen=True, slots=True)
class StopSalesFetchResult:
    unit_uuids: list[UUID]
    stop_sales: list[StopSaleByIngredient] | None = None
    exception: Exception | None = None


@dataclass(frozen=True, slots=True)
class StopSalesFetchAllResult:
    stop_sales: list[StopSaleByIngredient]
    error_unit_uuids: set[UUID]


class StopSalesFetcher:

    def __init__(self, connection: DodoIsConnection):
        self.__connection = connection
        self.__tasks_registry: set[AccessTokenAndUnitUuids] = set()

    def register_task(
            self,
            *,
            access_token: SecretStr,
            unit_uuids: Iterable[UUID],
    ) -> None:
        for unit_uuids_batch in batched(unit_uuids, batch_size=30):
            self.__tasks_registry.add((access_token, tuple(unit_uuids_batch)))

    async def _get_units_stop_sales(
            self,
            *,
            access_token: SecretStr,
            unit_uuids: Iterable[UUID],
            from_date: datetime,
            to_date: datetime,
    ) -> StopSalesFetchResult:
        unit_uuids = list(unit_uuids)

        stop_sales: list[StopSaleByIngredient] = []

        try:
            logger.debug(
                f'Fetching stop sales',
                extra={'unit_uuids': unit_uuids},
            )
            response = await self.__connection.get_stop_sales_by_ingredients(
                access_token=access_token.get_secret_value(),
                unit_uuids=unit_uuids,
                from_date=from_date,
                to_date=to_date,
            )
            logger.debug(
                f'Fetched stop sales',
                extra={
                    'status_code': response.status_code,
                    'body': response.text,
                },
            )

            stop_sales += parse_stop_sales_by_ingredients_response(response)

        except Exception as error:
            return StopSalesFetchResult(
                unit_uuids=unit_uuids,
                exception=error,
            )

        return StopSalesFetchResult(
            unit_uuids=unit_uuids,
            stop_sales=stop_sales,
        )

    async def fetch_all(
            self,
            from_date: datetime,
            to_date: datetime,
    ) -> StopSalesFetchAllResult:
        tasks: list[asyncio.Task[StopSalesFetchResult]] = []
        async with asyncio.TaskGroup() as task_group:
            for access_token, unit_uuids in self.__tasks_registry:
                task = self._get_units_stop_sales(
                    access_token=access_token,
                    unit_uuids=unit_uuids,
                    from_date=from_date,
                    to_date=to_date,
                )
                tasks.append(task_group.create_task(task))

        stop_sales: list[StopSaleByIngredient] = []
        error_unit_uuids: set[UUID] = set()
        for task in tasks:
            result = task.result()
            if result.exception is None:
                stop_sales += result.stop_sales
            else:
                logger.exception(
                    f'Failed to fetch stop sales',
                    exc_info=result.exception,
                    extra={'unit_uuids': result.unit_uuids},
                )
                error_unit_uuids.update(result.unit_uuids)

        return StopSalesFetchAllResult(
            stop_sales=stop_sales,
            error_unit_uuids=error_unit_uuids,
        )

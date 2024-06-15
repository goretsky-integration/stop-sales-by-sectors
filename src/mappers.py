from collections import defaultdict
from collections.abc import Iterable
from typing import TypeAlias
from uuid import UUID

from models import (
    AccountUnits,
    Event,
    EventPayloadStopSale,
    EventPayloadStopSalesGroupedByReason,
    EventPayloadUnitStopSales,
    StopSaleBySector,
    Unit,
)

__all__ = (
    'map_stop_sales_to_events',
    'map_events_payload_stop_sales_grouped_by_reason',
    'group_stop_sales_by_reason',
    'group_stop_sales_by_unit_uuid_and_name',
    'include_empty_units',
    'map_accounts_units_to_units',
)

UnitUUIDAndName: TypeAlias = tuple[UUID, str]
StopSalesByIngredients: TypeAlias = Iterable[StopSaleBySector]
StopSalesByIngredientsList: TypeAlias = list[StopSaleBySector]


def group_stop_sales_by_reason(
        stop_sales: StopSalesByIngredients,
) -> dict[str, StopSalesByIngredientsList]:
    reason_to_stop_sales: defaultdict[str, StopSalesByIngredientsList] = (
        defaultdict(list)
    )

    for stop_sale in stop_sales:
        reason_to_stop_sales[stop_sale.reason].append(stop_sale)

    return dict(reason_to_stop_sales)


def group_stop_sales_by_unit_uuid_and_name(
        stop_sales: StopSalesByIngredients,
) -> dict[UnitUUIDAndName, list[StopSaleBySector]]:
    unit_uuid_and_name_to_stop_sales: (
        defaultdict[UnitUUIDAndName, list[StopSaleBySector]]
    ) = defaultdict(list)

    for stop_sale in stop_sales:
        unit_uuid_and_name = (stop_sale.unit_uuid, stop_sale.unit_name)
        unit_uuid_and_name_to_stop_sales[unit_uuid_and_name].append(stop_sale)

    return dict(unit_uuid_and_name_to_stop_sales)


def map_events_payload_stop_sales_grouped_by_reason(
        stop_sales: StopSalesByIngredients,
) -> list[EventPayloadStopSalesGroupedByReason]:
    reason_to_stop_sales = group_stop_sales_by_reason(stop_sales)

    result: list[EventPayloadStopSalesGroupedByReason] = []
    for reason, stop_sales_grouped_by_reason in reason_to_stop_sales.items():
        event_payload_stop_sales = [
            EventPayloadStopSale(
                ingredient_name=stop_sale.ingredient_name,
                started_at=stop_sale.started_at_local,
            )
            for stop_sale in stop_sales_grouped_by_reason
        ]

        result.append(
            EventPayloadStopSalesGroupedByReason(
                reason=reason,
                stop_sales=event_payload_stop_sales,
            )
        )

    return result


def map_stop_sales_to_events(
        stop_sales: StopSalesByIngredients,
) -> list[Event]:
    unit_uuid_and_name_to_stop_sales = group_stop_sales_by_unit_uuid_and_name(
        stop_sales=stop_sales,
    )

    result: list[Event] = []
    for (unit_uuid, unit_name), stop_sales_grouped_by_unit_name in (
            unit_uuid_and_name_to_stop_sales.items()
    ):
        event_payload_stop_sales_grouped_by_reasons = (
            map_events_payload_stop_sales_grouped_by_reason(
                stop_sales=stop_sales_grouped_by_unit_name,
            )
        )

        event_payload_unit_stop_sales = EventPayloadUnitStopSales(
            unit_name=unit_name,
            stop_sales_grouped_by_reasons=(
                event_payload_stop_sales_grouped_by_reasons
            ),
        )
        event = Event(
            unit_ids=unit_uuid,
            payload=event_payload_unit_stop_sales,
        )
        result.append(event)

    return result


def include_empty_units(
        *,
        events: Iterable[Event],
        units: Iterable[Unit],
) -> list[Event]:
    events = list(events)
    existing_units = {event.unit_ids for event in events}

    empty_events: list[Event] = []
    for unit in units:
        if unit.uuid not in existing_units:
            event = Event(
                unit_ids=unit.uuid,
                payload=EventPayloadUnitStopSales(
                    unit_name=unit.name,
                    stop_sales_grouped_by_reasons=[],
                ),
            )
            empty_events.append(event)

    return events + empty_events


def map_accounts_units_to_units(
        accounts_units: Iterable[AccountUnits],
) -> list[Unit]:
    return [
        unit
        for account_units in accounts_units
        for unit in account_units.units
    ]

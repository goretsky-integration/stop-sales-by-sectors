from collections import defaultdict
from collections.abc import Iterable

from models import (
    AccountUnits,
    Event,
    EventPayload,
    EventPayloadStopSale,
    StopSaleBySector,
    Unit,
)

__all__ = (
    'map_stop_sales_to_events',
    'group_stop_sales_by_unit_name',
    'map_accounts_units_to_units',
)


def group_stop_sales_by_unit_name(
        stop_sales: Iterable[StopSaleBySector],
) -> dict[str, list[StopSaleBySector]]:
    unit_name_to_stop_sales: defaultdict[str, list[StopSaleBySector]] = (
        defaultdict(list)
    )

    for stop_sale in stop_sales:
        unit_name_to_stop_sales[stop_sale.unit_name].append(stop_sale)

    return dict(unit_name_to_stop_sales)


def map_stop_sales_to_events(
        stop_sales: Iterable[StopSaleBySector],
) -> list[Event]:
    unit_name_to_uuid = {
        stop_sale.unit_name: stop_sale.unit_uuid
        for stop_sale in stop_sales
    }
    unit_name_to_stop_sales = group_stop_sales_by_unit_name(stop_sales)

    events: list[Event] = []
    for unit_name, grouped_stop_sales in unit_name_to_stop_sales.items():
        unit_uuid = unit_name_to_uuid[unit_name]

        event_payload_stop_sales = [
            EventPayloadStopSale(
                started_at=stop_sale.started_at_local,
                sector_name=stop_sale.sector_name,
            )
            for stop_sale in grouped_stop_sales
        ]
        event_payload = EventPayload(
            unit_name=unit_name,
            stop_sales=event_payload_stop_sales,
        )
        event = Event(unit_ids=unit_uuid, payload=event_payload)
        events.append(event)

    return events


def map_accounts_units_to_units(
        accounts_units: Iterable[AccountUnits],
) -> list[Unit]:
    return [
        unit
        for account_units in accounts_units
        for unit in account_units.units
    ]

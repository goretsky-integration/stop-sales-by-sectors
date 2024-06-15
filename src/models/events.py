from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, conlist

__all__ = (
    'EventPayloadStopSale',
    'EventPayloadUnitStopSales',
    'EventPayloadStopSalesGroupedByReason',
    'Event',
)


class EventPayloadStopSale(BaseModel):
    started_at: datetime
    ingredient_name: str


class EventPayloadStopSalesGroupedByReason(BaseModel):
    reason: str
    stop_sales: conlist(EventPayloadStopSale, min_length=1)


class EventPayloadUnitStopSales(BaseModel):
    unit_name: str
    stop_sales_grouped_by_reasons: list[EventPayloadStopSalesGroupedByReason]


class Event(BaseModel):
    type: str = Field(default='INGREDIENTS_STOP_SALES', frozen=True)
    unit_ids: UUID
    payload: EventPayloadUnitStopSales

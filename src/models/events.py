from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, conlist

__all__ = (
    'EventPayloadStopSale',
    'EventPayload',
    'Event',
)


class EventPayloadStopSale(BaseModel):
    started_at: datetime
    sector_name: str


class EventPayload(BaseModel):
    unit_name: str
    stop_sales: conlist(EventPayloadStopSale, min_length=1)


class Event(BaseModel):
    type: str = Field(default='SECTOR_STOP_SALES', frozen=True)
    unit_ids: UUID
    payload: EventPayload

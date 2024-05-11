import datetime
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ('StopSaleByIngredient',)


class StopSaleByIngredient(BaseModel):
    id: UUID
    unit_uuid: UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    ingredient_name: str = Field(alias='ingredientName')
    reason: str
    started_at_local: datetime.datetime = Field(alias='startedAtLocal')
    ended_at_local: datetime.datetime = Field(alias='endedAtLocal')
    stoppedd_by_user_id: UUID = Field(alias='stoppedByUserId')
    resumed_by_user_id: UUID = Field(alias='resumedByUserId')
    started_at: datetime.datetime = Field(alias='startedAt')
    ended_at: datetime.datetime = Field(alias='endedAt')

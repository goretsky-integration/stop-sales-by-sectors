from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ('StopSaleByIngredient',)


class StopSaleByIngredient(BaseModel):
    id: UUID
    unit_uuid: Annotated[UUID, Field(validation_alias='unitId')]
    unit_name: Annotated[str, Field(validation_alias='unitName')]
    ingredient_name: Annotated[str, Field(validation_alias='ingredientName')]
    reason: str
    started_at_local: Annotated[
        datetime,
        Field(validation_alias='startedAtLocal'),
    ]
    ended_at_local: Annotated[
        datetime | None,
        Field(validation_alias='endedAtLocal'),
    ]
    stopped_by_user_id: Annotated[
        UUID,
        Field(validation_alias='stoppedByUserId'),
    ]
    resumed_by_user_id: Annotated[
        UUID | None,
        Field(validation_alias='resumedByUserId'),
    ]

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ('StopSaleBySector',)


class StopSaleBySector(BaseModel):
    id: UUID
    unit_uuid: Annotated[UUID, Field(validation_alias='unitId')]
    unit_name: Annotated[str, Field(validation_alias='unitName')]
    sector_name: Annotated[str, Field(validation_alias='sectorName')]
    is_sub_sector: Annotated[bool, Field(validation_alias='isSubSector')]
    started_at_local: Annotated[
        datetime,
        Field(validation_alias='startedAtLocal'),
    ]
    ended_at_local: Annotated[
        datetime | None,
        Field(validation_alias='endedAtLocal'),
    ]
    suspended_by_user_id: Annotated[
        UUID,
        Field(validation_alias='suspendedByUserId'),
    ]
    resumed_by_user_id: Annotated[
        UUID | None,
        Field(validation_alias='resumedUserId'),
    ]

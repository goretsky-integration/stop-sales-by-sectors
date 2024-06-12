import datetime
from dataclasses import dataclass
from typing import Self
from zoneinfo import ZoneInfo

__all__ = ('Period',)


@dataclass(frozen=True, slots=True)
class Period:
    from_date: datetime.datetime
    to_date: datetime.datetime

    @classmethod
    def today_to_this_moment(cls, timezone: ZoneInfo) -> Self:
        now = datetime.datetime.now(timezone)
        return cls(
            from_date=now.replace(hour=0, minute=0, second=0, microsecond=0),
            to_date=now,
        )

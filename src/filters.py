from datetime import datetime
from typing import Protocol

__all__ = ('is_not_ended',)


class HasEndedAt(Protocol):
    ended_at: datetime | None


def is_not_ended(item: HasEndedAt) -> bool:
    return item.ended_at is None

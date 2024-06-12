from pydantic import BaseModel, conlist

from models import Unit

__all__ = ('AccountUnits',)


class AccountUnits(BaseModel):
    account_name: str
    units: conlist(Unit, min_length=1)

import itertools
import operator
from collections.abc import Iterable
from typing import Protocol, TypeVar

import httpx
from pydantic import TypeAdapter

from models import Unit

__all__ = ('parse_units_response', 'group_by_dodo_is_api_account_name')


class HasDodoIsApiAccountName(Protocol):
    dodo_is_api_account_name: str


HasDodoIsApiAccountNameT = TypeVar(
    'HasDodoIsApiAccountNameT',
    bound=HasDodoIsApiAccountName,
)


def parse_units_response(response: httpx.Response) -> list[Unit]:
    type_adapter = TypeAdapter(list[Unit])
    response_data: dict = response.json()
    return type_adapter.validate_python(response_data['units'])


def group_by_dodo_is_api_account_name(
        items: Iterable[HasDodoIsApiAccountNameT]
) -> Iterable[tuple[str, Iterable[HasDodoIsApiAccountNameT]]]:
    return itertools.groupby(
        iterable=items,
        key=operator.attrgetter('dodo_is_api_account_name'),
    )

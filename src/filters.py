from collections.abc import Iterable

from models import StopSaleByIngredient

__all__ = ('filter_not_ended_stop_sales',)


def filter_not_ended_stop_sales(
        stop_sales: Iterable[StopSaleByIngredient],
) -> list[StopSaleByIngredient]:
    return [
        stop_sale for stop_sale in stop_sales
        if stop_sale.ended_at_local is None
    ]

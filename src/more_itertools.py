import itertools
from collections.abc import Generator, Iterable
from typing import TypeVar

__all__ = ('batched',)

T = TypeVar('T')


def batched(
        items: Iterable[T],
        batch_size: int,
) -> Generator[list[T], None, None]:
    """
    Yield batches of n items from the iterable.

    >>> list(batched([1, 2, 3, 4, 5, 6], 3))
    [[1, 2, 3], [4, 5, 6]]
    """
    iterable = iter(items)
    while True:
        batch = list(itertools.islice(iterable, batch_size))
        if not batch:
            return
        yield batch

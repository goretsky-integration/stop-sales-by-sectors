import asyncio

from fast_depends import Depends, inject

from context.units_storage import UnitsStorageContext
from dependencies import get_units_storage_context


@inject
async def main(
        units_storage_context: UnitsStorageContext = Depends(
            get_units_storage_context,
            use_cache=False,
        )
) -> None:
    units = units_storage_context.get_units()


if __name__ == '__main__':
    asyncio.run(main())

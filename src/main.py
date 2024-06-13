import asyncio

from fast_depends import Depends, inject

from config import Config, get_config
from connections.auth_credentials_storage import (
    AuthCredentialsStorageConnection,
)
from connections.dodo_is import DodoIsConnection
from context.auth_credentials_storage import AuthCredentialsFetchUnitOfWork
from context.dodo_is import StopSalesFetchUnitOfWork
from dependencies import (
    get_auth_credentials_storage_connection,
    get_dodo_is_connection,
)
from logger import create_logger
from models import AccountUnits
from time_helpers import Period
from units import load_units

logger = create_logger('main')


@inject
async def main(
        auth_credentials_connection: AuthCredentialsStorageConnection = Depends(
            get_auth_credentials_storage_connection,
        ),
        dodo_is_connection: DodoIsConnection = Depends(get_dodo_is_connection),
        accounts_units: list[AccountUnits] = Depends(load_units),
        config: Config = Depends(get_config),
) -> None:
    period = Period.today_to_this_moment(timezone=config.timezone)

    auth_credentials_fetch_unit_of_work = AuthCredentialsFetchUnitOfWork(
        connection=auth_credentials_connection,
    )
    for account_units in accounts_units:
        auth_credentials_fetch_unit_of_work.register_task(
            account_name=account_units.account_name,
        )

    accounts_tokens = await auth_credentials_fetch_unit_of_work.commit()
    account_name_to_access_token = {
        account_tokens.account_name: account_tokens.access_token
        for account_tokens in accounts_tokens
    }

    stop_sales_fetch_unit_of_work = StopSalesFetchUnitOfWork(
        connection=dodo_is_connection,
    )

    for account_units in accounts_units:
        access_token = account_name_to_access_token[account_units.account_name]
        unit_uuids = [unit.uuid for unit in account_units.units]

        stop_sales_fetch_unit_of_work.register_task(
            access_token=access_token,
            unit_uuids=unit_uuids,
        )

    stop_sales = await stop_sales_fetch_unit_of_work.commit(
        from_date=period.from_date,
        to_date=period.to_date,
    )

    logger.debug('Stop sales', extra={
        'stop_sales': stop_sales,
    })


if __name__ == '__main__':
    asyncio.run(main())

import argparse
import asyncio

from fast_depends import Depends, inject

from config import Config, get_config
from connections.auth_credentials_storage import (
    AuthCredentialsStorageConnection,
)
from connections.dodo_is import DodoIsConnection
from connections.event_publisher import EventPublisher
from connections.stop_sales_state import StopSalesStateManager
from context.auth_credentials_storage import AuthCredentialsFetcher
from context.dodo_is import StopSalesFetcher
from dependencies import (
    get_auth_credentials_storage_connection,
    get_dodo_is_connection, get_event_publisher, get_stop_sales_state_manager,
)
from filters import filter_not_ended_stop_sales
from logger import create_logger, setup_logging
from mappers import (
    include_empty_units, map_accounts_units_to_units,
    map_stop_sales_to_events,
)
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
        event_publisher: EventPublisher = Depends(get_event_publisher),
        stop_sales_state_manager: StopSalesStateManager = Depends(
            get_stop_sales_state_manager,
        ),
) -> None:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        '--remember',
        action='store_true',
        help='Save stop sale\'s IDs in the local storage',
    )
    argument_parser.add_argument(
        '--ignore-remembered',
        action='store_true',
        help='Ignore if stop sale\'s ID in the local storage',
    )
    argument_parser.add_argument(
        '--with-empty-units',
        action='store_true',
        help='Create event even if unit has no stop sales',
    )

    arguments = argument_parser.parse_args()

    setup_logging()

    period = Period.today_to_this_moment(timezone=config.timezone)

    auth_credentials_fetch_unit_of_work = AuthCredentialsFetcher(
        connection=auth_credentials_connection,
    )
    for account_units in accounts_units:
        auth_credentials_fetch_unit_of_work.register_account_name(
            account_name=account_units.account_name,
        )

    accounts_tokens = await auth_credentials_fetch_unit_of_work.fetch_all()
    account_name_to_access_token = {
        account_tokens.account_name: account_tokens.access_token
        for account_tokens in accounts_tokens
    }

    stop_sales_fetch_unit_of_work = StopSalesFetcher(
        connection=dodo_is_connection,
    )

    for account_units in accounts_units:
        access_token = account_name_to_access_token[account_units.account_name]
        unit_uuids = [unit.uuid for unit in account_units.units]

        stop_sales_fetch_unit_of_work.register_task(
            access_token=access_token,
            unit_uuids=unit_uuids,
        )

    stop_sales_fetch_result = await stop_sales_fetch_unit_of_work.fetch_all(
        from_date=period.from_date,
        to_date=period.to_date,
    )

    stop_sales = stop_sales_fetch_result.stop_sales

    if arguments.ignore_remembered:
        stop_sales = await stop_sales_state_manager.filter(stop_sales)

    if arguments.remember and stop_sales:
        await stop_sales_state_manager.save(stop_sales)

    for unit_uuid in stop_sales_fetch_result.error_unit_uuids:
        logger.error(
            'Failed to fetch stop sales',
            extra={'unit_uuid': unit_uuid},
        )

    not_ended_stop_sales = filter_not_ended_stop_sales(stop_sales)

    events = map_stop_sales_to_events(not_ended_stop_sales)

    if arguments.with_empty_units:
        events = include_empty_units(
            events=events,
            units=map_accounts_units_to_units(accounts_units),
        )

    logger.debug('Stop sales', extra={
        'stop_sales': not_ended_stop_sales,
    })

    await event_publisher.publish_all(events)


if __name__ == '__main__':
    asyncio.run(main())

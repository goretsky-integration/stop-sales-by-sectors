from collections.abc import Iterable

from faststream.rabbit import RabbitBroker

from models import Event

__all__ = ('EventPublisher',)


class EventPublisher:

    def __init__(self, broker: RabbitBroker):
        self.__broker = broker

    async def publish_all(self, events: Iterable[Event]) -> None:
        for event in events:
            await self.__broker.publish(
                message=event.model_dump(),
                queue='specific-units-event',
            )

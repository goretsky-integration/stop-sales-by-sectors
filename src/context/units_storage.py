from connections.units_storage import UnitsStorageConnection
from models import Unit
from parsers.units import parse_units_response

__all__ = ('UnitsStorageContext',)


class UnitsStorageContext:

    def __init__(self, connection: UnitsStorageConnection):
        self.__connection = connection

    def get_units(self) -> list[Unit]:
        response = self.__connection.get_units()
        return parse_units_response(response)

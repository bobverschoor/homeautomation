from entiteiten.telegram import Telegram
from persistence.database_gateway import DatabaseGateway
from sensor.dsmr_50_device import DSMR_50
from sensor.slimmemeter_gateway import SlimmemeterGateway


class EnergieMeterController:
    def __init__(self):
        self._slimmemeter = SlimmemeterGateway()
        self._slimmemeter.p1 = DSMR_50()
        self._databasebase = DatabaseGateway()
        self._telegram = Telegram()
        self._meetwaarden = []

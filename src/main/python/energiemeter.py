from persistence.database_gateway import DatabaseGateway
from sensor.dsmr_50_device import DSMR_50
from sensor.slimmemeter_gateway import SlimmemeterGateway


class EnergieMeterController:
    def __init__(self):
        self._slimmemeter = SlimmemeterGateway()
        self._slimmemeter.p1 = DSMR_50()
        self._databasebase = DatabaseGateway("p1meter")

    def collect_store(self):
        meetwaarden = self._slimmemeter.get_meetwaarden()
        for meetwaarde in meetwaarden:
            self._databasebase.entiteiten = meetwaarde
        self._databasebase.store()


if __name__ == "__main__":
    EnergieMeterController().collect_store()
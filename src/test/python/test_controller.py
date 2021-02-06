import unittest

from entiteiten.electra import Electra
from entiteiten.gas import Gas
from mock_influxdb_device import MockInFluxDBDevice
from mock_p1_device import MockP1Device
from persistence.database_gateway import DatabaseGateway
from sensor.slimmemeter_gateway import SlimmemeterGateway
from verlading_controller import Verlader


def get_a_electra():
    electra = Electra()
    electra.richting = Electra.VERBRUIKT
    electra.tarief = Electra.LAAGTARIEF
    electra.waarde = 34224
    return electra


def get_a_gas():
    gas = Gas()
    gas.waarde = 4312
    return gas


class MockDatabaseGateway(DatabaseGateway):

    def store(self):
        pass


class MockSlimmemeterGateway(SlimmemeterGateway):
   def _collect_data(self):
        electra = {"low": {}}
        electra["low"]["consumed"] = 16351.117
        electra["low"]["produced"] = 1.804
        electra["high"] = {}
        electra["high"]["consumed"] = 20121.471
        electra["high"]["produced"] = 0.007
        electra["timestamp"] = 1601391600
        gas = {"m3": 7368.67, "timestamp": 1601391600}
        self._set_electra(electra)
        self._set_gas(gas)


class TestVerladingController(unittest.TestCase):
    def test_get1meting_and_store(self):
        verlader = Verlader()
        mock_db = MockDatabaseGateway()
        verlader.database = mock_db
        verlader.slimmemeter = MockSlimmemeterGateway()
        verlader.collect()
        verlader.store()
        expected_entiteiten = [
            "tarief: laag, richting: verbruikt, Wh: 16351117, tijdstip: 2021-01-02 08:46:23.986394+00:00",
            "tarief: laag, richting: geleverd, Wh: 1804, tijdstip: 2021-01-02 08:46:23.986408+00:00",
            "tarief: hoog, richting: verbruikt, Wh: 20121471, tijdstip: 2021-01-02 08:46:23.986413+00:00",
            "tarief: hoog, richting: geleverd, Wh: 7, tijdstip: 2021-01-02 08:46:23.986418+00:00",
            "m3: 7368.67, tijdstip: 2020-09-29 17:00:00"]
        actual_entiteiten = []
        for entiteit in mock_db.entiteiten:
            actual_entiteiten.append(str(entiteit))
        self.assertEqual(expected_entiteiten, actual_entiteiten)
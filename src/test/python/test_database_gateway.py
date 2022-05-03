import unittest

from entiteiten.electra import Electra
from entiteiten.gas import Gas
from persistence.database_gateway import DatabaseGateway
from persistence.influxdb_device import InFluxDBDevice


class MockInFluxDBDevice(InFluxDBDevice):
    # noinspection PyMissingConstructor
    def __init__(self):
        self._meetwaarde = None

    def write(self, meetwaarde):
        self._meetwaarde = meetwaarde
        return True


def get_a_electra():
    electra = Electra(waarde=34224, richting=Electra.VERBRUIKT, tarief=Electra.LAAGTARIEF, tags={})
    return electra


class TestDatabasegateway(unittest.TestCase):
    def test_store_electra_gas(self):
        db = DatabaseGateway("test")
        db.repository = MockInFluxDBDevice()
        electra = get_a_electra()
        db.entiteiten.append(electra)
        gas = Gas(waarde=4312, tags={})
        db.entiteiten.append(gas)
        db.store()
        self.assertEqual([
            {"measurement": electra.eenheid,
             "tags": electra.tags,
             "time": electra.timestamp,
             "fields": {"meetwaarde": electra.waarde}},
            {"measurement": gas.eenheid,
             "tags": {},
             "time": gas.timestamp,
             "fields": {"meetwaarde": gas.waarde}}],
            db.repository._meetwaarde)

    # def test_integratie(self):
    #     db = DatabaseGateway()
    #     db.repository.drop_database()
    #     electra = get_a_electra()
    #     db.entiteiten.append(electra)
    #     gas = Gas()
    #     gas.waarde = 4312
    #     db.entiteiten.append(gas)
    #     db.store()
    #     items = db.repository.get_all_items()
    #     print(items)


if __name__ == '__main__':
    unittest.main()

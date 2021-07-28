import unittest

from entiteiten.electra import Electra
from entiteiten.gas import Gas
from mock_influxdb_device import MockInFluxDBDevice
from persistence.database_gateway import DatabaseGateway


def get_a_electra():
    electra = Electra()
    electra.richting = Electra.VERBRUIKT
    electra.tarief = Electra.LAAGTARIEF
    electra.waarde = 34224
    return electra


class TestDatabasegateway(unittest.TestCase):
    def test_store_electra_gas(self):
        db = DatabaseGateway("test")
        db.repository = MockInFluxDBDevice()
        electra = get_a_electra()
        db.entiteiten.append(electra)
        gas = Gas()
        gas.waarde = 4312
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

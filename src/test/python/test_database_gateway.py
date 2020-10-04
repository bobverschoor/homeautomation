import unittest

from entiteiten.electra import Electra
from persistence.database_gateway import DatabaseGateway


class TestDatabasegateway(unittest.TestCase):
    def test_store_electra(self):
        electra = Electra()
        electra.richting = Electra.HOOGTARIEF
        electra.tarief = Electra.LAAGTARIEF
        electra.wh = 34224
        db = DatabaseGateway()
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()

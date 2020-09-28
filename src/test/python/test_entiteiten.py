import datetime
import unittest

from entiteiten.electra import Electra
from entiteiten.gas import Gas


class TestEntiteiten(unittest.TestCase):
    def test_correct_electra(self):
        e = Electra()
        e.tarief = Electra.HOOGTARIEF
        e.richting = Electra.CONSUMENT
        e.wh = 1000
        self.assertEqual("tarief: hoog, richting: consument, Wh: 1000, time: " + str(e._timestamp), str(e))

    def test_incorrect_e_fields_expects_exception(self):
        e = Electra()
        with self.assertRaises(ValueError):
            e.tarief = "HIGH"
        with self.assertRaises(ValueError):
            e.richting = "UP"
        with self.assertRaises(ValueError):
            e.wh = -5

    def test_correct_gas(self):
        g = Gas()
        g.m3 = 1000
        g.timestamp = datetime.datetime.now(datetime.timezone.utc)
        self.assertEqual("m3: 1000, time: " + str(g._timestamp), str(g))

    def test_incorrect_g_fields_expects_exception(self):
        g = Gas()
        with self.assertRaises(ValueError):
            g.m3 = -3
        with self.assertRaises(ValueError):
            g.timestamp = -1


if __name__ == '__main__':
    unittest.main()

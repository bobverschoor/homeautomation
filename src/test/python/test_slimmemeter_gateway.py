import unittest

from entiteiten.electra import Electra
from entiteiten.gas import Gas


class TestSlimmemeterGateway(unittest.TestCase):
    def test_get_electra(self):
        sm = SlimmemeterGateway()
        sm.get_electra()
        self.assertEqual("", sm.e)
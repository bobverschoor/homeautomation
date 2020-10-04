import unittest

from mock_p1_device import MockP1Device
from sensor.slimmemeter_gateway import SlimmemeterGateway


class TestSlimmemeterGateway(unittest.TestCase):
    def test_get_electra(self):
        sm = SlimmemeterGateway()
        sm.p1 = MockP1Device('p1_test_ok.json')
        self.assertEqual("tarief: laag, richting: verbruikt, Wh: 16351117, tijdstip: " + str(sm.electra[0]._timestamp),
                         str(sm.electra[0]))
        self.assertEqual("tarief: laag, richting: geleverd, Wh: 1804, tijdstip: " + str(sm.electra[1]._timestamp),
                         str(sm.electra[1]))
        self.assertEqual("tarief: hoog, richting: verbruikt, Wh: 20121471, tijdstip: " + str(sm.electra[2]._timestamp),
                         str(sm.electra[2]))
        self.assertEqual("tarief: hoog, richting: geleverd, Wh: 7, tijdstip: " + str(sm.electra[3]._timestamp),
                         str(sm.electra[3]))
        self.assertEqual("m3: 7368.67, tijdstip: " + str(sm.gas[0]._timestamp),
                         str(sm.gas[0]))

    def test_get_gas(self):
        sm = SlimmemeterGateway()
        sm.p1 = MockP1Device('p1_test_ok.json')
        self.assertEqual("m3: 7368.67, tijdstip: " + str(sm.gas[0]._timestamp),
                         str(sm.gas[0]))

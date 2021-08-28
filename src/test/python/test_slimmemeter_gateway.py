import unittest

from mock_dsmr_device import Mock_DSMR_50_Device, nr_of_atts
from device.slimmemeter_gateway import SlimmemeterGateway


class TestSlimmemeterGateway(unittest.TestCase):

    def test_get_meetwaarde(self):
        sm = SlimmemeterGateway()
        sm.p1 = Mock_DSMR_50_Device()
        meetwaarden = sm.get_meetwaarden()
        self.assertEqual(nr_of_atts(), len(meetwaarden))
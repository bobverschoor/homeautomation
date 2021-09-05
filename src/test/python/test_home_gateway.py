import unittest

from device.hue_bridge_device import HueBridgeDevice
from entiteiten.licht import Licht
from gateways.woning_gateway import WoningGateway


class MockBridge(HueBridgeDevice):
    def __init__(self):
        super().__init__({HueBridgeDevice.CONFIG_HUEBRIDGE:
                              {HueBridgeDevice.CONFIG_IP:"", HueBridgeDevice.CONFIG_USERNAME:""}})

    def get_alle_lichten(self):
        licht = Licht("1")
        licht.naam = "plafond lamp"
        licht.aan = True
        return [licht]


class WoningGatewayTest(unittest.TestCase):
    def test_get_meetwaarden(self):
        hg = WoningGateway()
        hg.bridge = MockBridge()
        meetwaarden = hg.get_meetwaarden()
        self.assertEqual(1, len(meetwaarden))
        self.assertEqual("True licht_aan, tags: naam=plafond lamp", str(meetwaarden.pop()))


if __name__ == '__main__':
    unittest.main()

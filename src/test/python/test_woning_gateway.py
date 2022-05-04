import unittest

from device.sensor.hue_bridge_device import HueBridgeDevice
from entiteiten.licht import Licht
from entiteiten.sensor import Schakelaar
from gateways.woning_gateway import WoningGateway


class MockBridge(HueBridgeDevice):
    def __init__(self):
        super().__init__({HueBridgeDevice.CONFIG_HUEBRIDGE: {HueBridgeDevice.CONFIG_IP: "",
                                                             HueBridgeDevice.CONFIG_USERNAME: "",
                                                             HueBridgeDevice.CONFIG_ALERTGROUP: ""}})

    def get_alle_lichten(self):
        licht = Licht("1")
        licht.naam = "plafond lamp"
        licht.aan = True
        licht.unique_id = "00:17:88:01:04:55:54:7d-0b"
        return [licht]

    def get_alle_sensors(self):
        sensor = Schakelaar("1")
        sensor.naam = "schakelaar"
        sensor.unique_id = "00:17:88:01:04:55:54:7d-0c"
        sensor.bereikbaar = True
        sensor.batterijpercentage = 98
        sensor.knop_id = 2002
        return [sensor]


class WoningGatewayTest(unittest.TestCase):
    def test_get_meetwaarden(self):
        hg = WoningGateway()
        hg.bridge = MockBridge()
        meetwaarden = hg.get_meetwaarden()
        self.assertEqual(5, len(meetwaarden))
        self.assertEqual("2002 knop_event, tags: naam=schakelaar id=001788010455547d0c",
                         str(meetwaarden.pop()))
        self.assertEqual("True bereikbaar, tags: naam=schakelaar id=001788010455547d0c",
                         str(meetwaarden.pop()))
        self.assertEqual("98 batterijpercentage, tags: naam=schakelaar id=001788010455547d0c",
                         str(meetwaarden.pop()))
        self.assertEqual("False bereikbaar, tags: naam=plafond lamp id=001788010455547d0b",
                         str(meetwaarden.pop()))
        self.assertEqual("True licht_aan, tags: naam=plafond lamp id=001788010455547d0b",
                         str(meetwaarden.pop()))


if __name__ == '__main__':
    unittest.main()

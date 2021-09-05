import unittest

from device.hue_bridge_device import HueBridgeDevice, HueBridgeException
from mock_api import MockAPI


class HueBridgeDeviceException:
    pass


class HueBridgeTest(unittest.TestCase):
    def test_setup(self):
        self.assertRaises(HueBridgeException, HueBridgeDevice, {'test': ''})
        self.assertRaises(HueBridgeException, HueBridgeDevice, {HueBridgeDevice.CONFIG_HUEBRIDGE: {}})

    def test_get_all_lights(self):
        hue = HueBridgeDevice({HueBridgeDevice.CONFIG_HUEBRIDGE: {HueBridgeDevice.CONFIG_IP: "",
                                                                  HueBridgeDevice.CONFIG_USERNAME: ""}})
        mockapi = MockAPI()
        hue._getlights_api = mockapi
        mockapi.json = testdata
        lichten = hue.get_alle_lichten()
        self.assertEqual(5, len(lichten))
        licht = lichten.pop()
        self.assertEqual("00:17:88:01:04:55:54:7d-0b", licht.unique_id)
        licht = lichten.pop()
        self.assertEqual("Alice plafond lamp", licht.naam)
        licht = lichten.pop()
        self.assertFalse(licht.aan)
        licht = lichten.pop()
        self.assertTrue(licht.aan)
        licht = lichten.pop()
        self.assertFalse(licht.aan)


testdata = \
    '{"1": { "state": {"on": false, "bri": 254, "alert": "select", "mode": "homeautomation", "reachable": true}, ' \
    '"swupdate": {"state": "noupdates", "lastinstall": "2021-08-17T18:50:54"}, "type": "Dimmable light", ' \
    '"name": "Lamp gang beneden", "modelid": "LWB010", "manufacturername": "Signify Netherlands B.V.", ' \
    '"productname": "Hue white lamp", "capabilities": {"certified": true, "control": {"mindimlevel": 2000, ' \
    '"maxlumen": 806}, "streaming": {"renderer": false, "proxy": false}}, "config": {"archetype": "classicbulb", ' \
    '"function": "functional", "direction": "omnidirectional", "startup": {"mode": "safety", "configured": true}},' \
    '"uniqueid": "00:17:88:01:04:00:17:0d-0b", "swversion": "1.88.1", "swconfigid": "06BB83C8", ' \
    '"productid": "Philips-LWB010-1-A19DLv4"}, ' \
    '"2": {"state": {"on": true, "bri": 254, "alert": "lselect", ' \
    '"mode": "homeautomation", "reachable": true}, "swupdate": {"state": "readytoinstall", "lastinstall": null}, ' \
    '"type": "Dimmable light", "name": "Studiekamer", "modelid": "LWB010", "manufacturername": ' \
    '"Signify Netherlands B.V.", "productname": "Hue white lamp", "capabilities": {"certified": true, ' \
    '"control": {"mindimlevel": 5000, "maxlumen": 806}, "streaming": {"renderer": false, "proxy": false}}, ' \
    '"config": {"archetype": "classicbulb", "function": "functional", "direction": "omnidirectional"}, ' \
    '"uniqueid": "00:17:88:01:04:00:74:2e-0b", "swversion": "1.29.0_r21169", "swconfigid": "FF6681C4", "productid": ' \
    '"Philips-LWB010-1-A19DLv4"}, ' \
    '"3": {"state": {"on": false, "bri": 0, "alert": "null", "mode": "homeautomation", ' \
    '"reachable": false}, "swupdate": {"state": "notupdatable", "lastinstall": null}, "type": "Dimmable light", ' \
    '"name": "Hue white lamp 3", "modelid": "LWB010", "manufacturername": "Signify Netherlands B.V.", "productname": ' \
    '"Hue white lamp", "capabilities": {"certified": true, "control": {"mindimlevel": 5000, "maxlumen": 806}, ' \
    '"streaming": {"renderer": false, "proxy": false}}, "config": {"archetype": "classicbulb", "function": ' \
    '"functional", "direction": "omnidirectional"}, "uniqueid": "00:17:88:01:04:02:8a:fd-0b", "swversion": ' \
    '"1.29.0_r21169", "swconfigid": "FF6681C4", "productid": "Philips-LWB010-1-A19DLv4"}, ' \
    '"4": {"state": {"on": ' \
    'false, "bri": 254, "ct": 366, "alert": "select", "colormode": "ct", "mode": "homeautomation", "reachable": ' \
    'true}, "swupdate": {"state": "noupdates", "lastinstall": "2021-08-06T18:45:45"}, "type": "Color temperature ' \
    'light", "name": "Alice plafond lamp", "modelid": "LTC001", "manufacturername": "Signify Netherlands B.V.", ' \
    '"productname": "Hue ambiance ceiling", "capabilities": {"certified": true, "control": {"mindimlevel": 100, ' \
    '"maxlumen": 2400, "ct": {"min": 153, "max": 454}}, "streaming": {"renderer": false, "proxy": false}}, ' \
    '"config": {"archetype": "ceilinground", "function": "functional", "direction": "downwards", "startup": {"mode": ' \
    '"safety", "configured": true}}, "uniqueid": "00:17:88:01:03:03:fe:2d-0b", "swversion": "1.88.1", "swconfigid": ' \
    '"064CDDDC", "productid": "ENA_LTC001_1_BeingCeiling_v1"}, ' \
    '"5": {"state": {"on": true, "bri": 1, "ct": 447, ' \
    '"alert": "select", "colormode": "ct", "mode": "homeautomation", "reachable": false}, "swupdate": {"state": ' \
    '"readytoinstall", "lastinstall": "2020-09-23T18:07:38"}, "type": "Color temperature light", "name": "Ben ' \
    'plafond lamp", "modelid": "LTC001", "manufacturername": "Signify Netherlands B.V.", "productname": "Hue ambiance '\
    'ceiling", "capabilities": {"certified": true, "control": {"mindimlevel": 100, "maxlumen": 2400, "ct": {"min": ' \
    '153, "max": 454}}, "streaming": {"renderer": false, "proxy": false}}, "config": {"archetype": "ceilinground", ' \
    '"function": "functional", "direction": "downwards", "startup": {"mode": "safety", "configured": true}}, ' \
    '"uniqueid": "00:17:88:01:04:55:54:7d-0b", "swversion": "1.50.2_r30933", "swconfigid": "19789229", "productid": ' \
    '"ENA_LTC001_1_BeingCeiling_v1"}} '

if __name__ == '__main__':
    unittest.main()

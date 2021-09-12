import time
import unittest

from device.hue_bridge_device import HueBridgeDevice, HueBridgeException
from entiteiten.licht import Licht
from mock_api import MockAPI


class HueBridgeTest(unittest.TestCase):
    def test_setup(self):
        self.assertRaises(HueBridgeException, HueBridgeDevice, {'test': ''})
        self.assertRaises(HueBridgeException, HueBridgeDevice, {HueBridgeDevice.CONFIG_HUEBRIDGE: {}})

    def test_get_all_lights(self):
        hue = HueBridgeDevice({HueBridgeDevice.CONFIG_HUEBRIDGE: {HueBridgeDevice.CONFIG_IP: "",
                                                                  HueBridgeDevice.CONFIG_USERNAME: "",
                                                                  HueBridgeDevice.CONFIG_ALERTGROUP: ""}})
        mockapi = MockAPI()
        hue._lichts_api = mockapi
        mockapi.json = testdata_lights
        lichten = hue.get_alle_lichten()
        self.assertEqual(5, len(lichten))
        licht = lichten.pop()
        self.assertEqual(5, licht.volgnr)
        self.assertEqual("00:17:88:01:04:55:54:7d-0b", licht.unique_id)
        self.assertFalse(licht.bereikbaar)
        licht = lichten.pop()
        self.assertEqual(4, licht.volgnr)
        self.assertEqual("Alice plafond lamp", licht.naam)
        self.assertTrue(licht.bereikbaar)
        licht = lichten.pop()
        self.assertEqual(3, licht.volgnr)
        self.assertFalse(licht.aan)
        self.assertFalse(licht.bereikbaar)
        licht = lichten.pop()
        self.assertEqual(2, licht.volgnr)
        self.assertTrue(licht.aan)
        self.assertTrue(licht.bereikbaar)
        licht = lichten.pop()
        self.assertEqual(1, licht.volgnr)
        self.assertFalse(licht.aan)
        self.assertTrue(licht.bereikbaar)

    def test_get_alle_lichten_in_groep(self):
        hue = HueBridgeDevice({HueBridgeDevice.CONFIG_HUEBRIDGE: {HueBridgeDevice.CONFIG_IP: "",
                                                                  HueBridgeDevice.CONFIG_USERNAME: "",
                                                                  HueBridgeDevice.CONFIG_ALERTGROUP: "onbekendegroep"}})
        mockapilight = MockAPI()
        mockapigroup = MockAPI()
        hue._lichts_api = mockapilight
        hue._groups_api = mockapigroup
        mockapigroup.json = testdata_groups
        mockapilight.json = testdata_lights
        lichten = hue.get_alle_lichten_in_groep()
        self.assertEqual(0, len(lichten))
        hue = HueBridgeDevice({HueBridgeDevice.CONFIG_HUEBRIDGE: {HueBridgeDevice.CONFIG_IP: "",
                                                                  HueBridgeDevice.CONFIG_USERNAME: "",
                                                                  HueBridgeDevice.CONFIG_ALERTGROUP: "Deurbel"}})
        mockapilight = MockAPI()
        mockapigroup = MockAPI()
        hue._lichts_api = mockapilight
        hue._groups_api = mockapigroup
        mockapigroup.json = testdata_groups
        mockapilight.json = testdata_lights
        lichten = hue.get_alle_lichten_in_groep()
        self.assertEqual(2, len(lichten))
        for licht in lichten:
            self.assertTrue(licht.naam in ["Lamp gang beneden", "Studiekamer"])

    def test_alert_lights(self):
        hue = HueBridgeDevice({HueBridgeDevice.CONFIG_HUEBRIDGE: {HueBridgeDevice.CONFIG_IP: "192.168.1.40",
                                                                  HueBridgeDevice.CONFIG_USERNAME: "demo",
                                                                  HueBridgeDevice.CONFIG_ALERTGROUP: "Deurbel",
                                                                  HueBridgeDevice.CONFIG_ALERTTIMES: 2}})
        mockapilight = MockAPI(hue._lichts_api._url)
        hue._lichts_api = mockapilight
        licht = Licht(3)
        licht.aan = False
        licht.naam = "studie"
        hue.alert_lights([licht])
        while len(mockapilight.record) < 3:
            # Due to threading wait some time to finish the thread by itself
            time.sleep(0.1)
        self.assertEqual(mockapilight.record.pop(), 'http://192.168.1.40/api/demo/lights/3/state?{"alert": "none"}')
        self.assertEqual(mockapilight.record.pop(), 'http://192.168.1.40/api/demo/lights/3/state?{"alert": "select"}')
        self.assertEqual(mockapilight.record.pop(), 'http://192.168.1.40/api/demo/lights/3/state?{"alert": "select"}')
        self.assertEqual(0, len(mockapilight.record))


testdata_lights = \
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


testdata_groups = \
    '{"1": {"name": "Woonkamer", "lights": [], "sensors": [], "type": "Room","state": {"all_on": false, ' \
        '"any_on": false}, "recycle": false, "class": "Other", "action": { "on": false, "alert": "none"}},' \
    '"2": {"name": "Alice Slaapkamer", "lights": ["4"],"sensors": [],"type": "Room", "state": { "all_on": true,' \
        '"any_on": true}, "recycle": false, "class": "Kids bedroom", "action": { "on": true, "bri": 254, "ct": 443,' \
        '"alert": "select", "colormode": "ct"}}, ' \
    '"3": {"name": "Studie kamer", "lights": ["2"], "sensors": [], "type": "Room", "state": { "all_on": false,' \
        '"any_on": false},"recycle": false, "class": "Office","action": {"on": false,"bri": 254,"alert": "select"}},' \
    '"4": {"name": "Ben Slaapkamer", "lights": ["5"], "sensors": [], "type": "Room","state": {"all_on": false,' \
        '"any_on": false},"recycle": false,"class": "Kids bedroom","action": {"on": false,"bri": 1,"ct": 447,' \
        '"alert": "select","colormode": "ct"}},' \
    '"5": {"name": "Gang Beneden","lights": ["1"],"sensors": [],"type": "Room","state": {"all_on": false,' \
        '"any_on": false},"recycle": false,"class": "Hallway","action": {"on": false,"bri": 254,"alert": "select"}},' \
    '"6": {"name": "Deurbel","lights": ["2","1"],"sensors": [],"type": "Zone","state": {"all_on": false,' \
        '"any_on": false},"recycle": false,"class": "Front door","action": {"on": false,"bri": 254,"alert": "select"}}}'


if __name__ == '__main__':
    unittest.main()

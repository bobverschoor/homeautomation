import time
import unittest

from device.sensor.hue_bridge_device import HueBridgeDevice, HueBridgeException
from entiteiten.licht import Licht
from entiteiten.sensor import TemperatuurSensor, LichtSensor, BewegingSchakelaar, Schakelaar
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
        lichten = hue.get_alle_lichten_in_alarmeergroep()
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
        lichten = hue.get_alle_lichten_in_alarmeergroep()
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

    def test_sensors(self):
        hue = HueBridgeDevice({HueBridgeDevice.CONFIG_HUEBRIDGE: {HueBridgeDevice.CONFIG_IP: "",
                                                                  HueBridgeDevice.CONFIG_USERNAME: "",
                                                                  HueBridgeDevice.CONFIG_ALERTGROUP: ""}})
        mockapisensors = MockAPI(hue._sensors_api._url)
        hue._sensors_api = mockapisensors
        mockapisensors.json = testdata_sensors
        sensors = hue.get_alle_sensors()
        self.assertEqual(len(sensors), 6)
        sensor_temperature = sensors.pop()
        self.assertTrue(isinstance(sensor_temperature, TemperatuurSensor))
        self.assertEqual(sensor_temperature.naam, 'Hue temperature sensor 1')
        self.assertEqual(sensor_temperature.unique_id, "00:17:88:01:0b:09:b1:e6-02-0402")
        self.assertEqual(sensor_temperature.bereikbaar, True)
        self.assertEqual(sensor_temperature.batterijpercentage, 100)
        self.assertEqual(str(sensor_temperature.tijdstip_meting), '2021-12-31 06:02:58')
        self.assertEqual(sensor_temperature.temperature_celsius, 17.60)
        sensor_light = sensors.pop()
        self.assertTrue(isinstance(sensor_light, LichtSensor))
        self.assertEqual(sensor_light.lichtniveau_lux, 0)
        self.assertEqual(sensor_light.lichtniveau, 0)
        self.assertEqual(sensor_light.lichtwaarde, "Nacht licht")
        sensor_aanwezigheid = sensors.pop()
        self.assertTrue(isinstance(sensor_aanwezigheid, BewegingSchakelaar))
        self.assertEqual(sensor_aanwezigheid.beweging_gesignaleerd, True)
        sensor_knop_1 = sensors.pop()
        self.assertTrue(isinstance(sensor_knop_1, Schakelaar))
        self.assertEqual(sensor_knop_1.knop_waarde, 'uit')
        self.assertEqual(sensor_temperature.batterijpercentage, 100)
        sensor_knop_2 = sensors.pop()
        self.assertTrue(isinstance(sensor_knop_2, Schakelaar))
        self.assertEqual(sensor_knop_2.knop_waarde, 'dimmer_omhoog')
        self.assertEqual(sensor_knop_2.batterijpercentage, 5)
        sensor_knop_3 = sensors.pop()
        self.assertTrue(isinstance(sensor_knop_3, Schakelaar))
        self.assertEqual(sensor_knop_3.knop_waarde, 'aan')
        self.assertEqual(sensor_knop_3.batterijpercentage, 98)


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
    'plafond lamp", "modelid": "LTC001", "manufacturername": "Signify Netherlands B.V.", "productname": "Hue ambiance ' \
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

testdata_sensors = \
    '{"1":{"state":{"daylight":false,"lastupdated":"2021-12-30T15:06:00"},"config":{"on":true,"configured":true,' \
    '"sunriseoffset":30,"sunsetoffset":-30},"name":"Daylight","type":"Daylight","modelid":"PHDL00",' \
    '"manufacturername":"Signify Netherlands B.V.","swversion":"1.0"},"2":{"state":{"buttonevent":1000,' \
    '"lastupdated":"2021-12-17T18:21:22"},"swupdate":{"state":"noupdates","lastinstall":"2019-10-27T17:56:55"},' \
    '"config":{"on":true,"battery":98,"reachable":true,"pending":[]},"name":"Gang beneden","type":"ZLLSwitch",' \
    '"modelid":"RWL021","manufacturername":"Signify Netherlands B.V.","productname":"Hue dimmer switch",' \
    '"diversityid":"73bbabea-3420-499a-9856-46bf437e119b","swversion":"6.1.1.28573",' \
    '"uniqueid":"00:17:88:01:06:73:2d:14-02-fc00","capabilities":{"certified":true,"primary":true,"inputs":[{' \
    '"repeatintervals":[800],"events":[{"buttonevent":1000,"eventtype":"initial_press"},{"buttonevent":1001,' \
    '"eventtype":"repeat"},{"buttonevent":1002,"eventtype":"short_release"},{"buttonevent":1003,' \
    '"eventtype":"long_release"}]},{"repeatintervals":[800],"events":[{"buttonevent":2000,' \
    '"eventtype":"initial_press"},{"buttonevent":2001,"eventtype":"repeat"},{"buttonevent":2002,' \
    '"eventtype":"short_release"},{"buttonevent":2003,"eventtype":"long_release"}]},{"repeatintervals":[800],' \
    '"events":[{"buttonevent":3000,"eventtype":"initial_press"},{"buttonevent":3001,"eventtype":"repeat"},' \
    '{"buttonevent":3002,"eventtype":"short_release"},{"buttonevent":3003,"eventtype":"long_release"}]},' \
    '{"repeatintervals":[800],"events":[{"buttonevent":4000,"eventtype":"initial_press"},{"buttonevent":4001,' \
    '"eventtype":"repeat"},{"buttonevent":4002,"eventtype":"short_release"},{"buttonevent":4003,' \
    '"eventtype":"long_release"}]}]}},"4":{"state":{"buttonevent":2002,"lastupdated":"2021-12-31T05:48:19"},' \
    '"swupdate":{"state":"noupdates","lastinstall":"2019-11-09T07:30:46"},"config":{"on":true,"battery":5,' \
    '"reachable":true,"pending":[]},"name":"Danica bed","type":"ZLLSwitch","modelid":"RWL021",' \
    '"manufacturername":"Signify Netherlands B.V.","productname":"Hue dimmer switch",' \
    '"diversityid":"73bbabea-3420-499a-9856-46bf437e119b","swversion":"6.1.1.28573",' \
    '"uniqueid":"00:17:88:01:02:c3:58:da-02-fc00","capabilities":{"certified":true,"primary":true,"inputs":[{' \
    '"repeatintervals":[800],"events":[{"buttonevent":1000,"eventtype":"initial_press"},{"buttonevent":1001,' \
    '"eventtype":"repeat"},{"buttonevent":1002,"eventtype":"short_release"},{"buttonevent":1003,' \
    '"eventtype":"long_release"}]},{"repeatintervals":[800],"events":[{"buttonevent":2000,' \
    '"eventtype":"initial_press"},{"buttonevent":2001,"eventtype":"repeat"},{"buttonevent":2002,' \
    '"eventtype":"short_release"},{"buttonevent":2003,"eventtype":"long_release"}]},{"repeatintervals":[800],' \
    '"events":[{"buttonevent":3000,"eventtype":"initial_press"},{"buttonevent":3001,"eventtype":"repeat"},' \
    '{"buttonevent":3002,"eventtype":"short_release"},{"buttonevent":3003,"eventtype":"long_release"}]},' \
    '{"repeatintervals":[800],"events":[{"buttonevent":4000,"eventtype":"initial_press"},{"buttonevent":4001,' \
    '"eventtype":"repeat"},{"buttonevent":4002,"eventtype":"short_release"},{"buttonevent":4003,' \
    '"eventtype":"long_release"}]}]}},"5":{"state":{"status":0,"lastupdated":"2021-12-31T05:48:29"},"config":{' \
    '"on":true,"reachable":true},"name":"Dimmer Switch 4 SceneCycle","type":"CLIPGenericStatus","modelid":"PHWA01",' \
    '"manufacturername":"Philips","swversion":"1.0","uniqueid":"WA0001","recycle":true},"6":{"state":{' \
    '"buttonevent":4002,"lastupdated":"2021-12-31T04:33:52"},"swupdate":{"state":"noupdates",' \
    '"lastinstall":"2019-10-27T17:50:27"},"config":{"on":true,"battery":13,"reachable":true,"pending":[]},' \
    '"name":"Toilet","type":"ZLLSwitch","modelid":"RWL021","manufacturername":"Signify Netherlands B.V.",' \
    '"productname":"Hue dimmer switch","diversityid":"73bbabea-3420-499a-9856-46bf437e119b",' \
    '"swversion":"6.1.1.28573","uniqueid":"00:17:88:01:04:af:6a:f9-02-fc00","capabilities":{"certified":true,' \
    '"primary":true,"inputs":[{"repeatintervals":[800],"events":[{"buttonevent":1000,"eventtype":"initial_press"},' \
    '{"buttonevent":1001,"eventtype":"repeat"},{"buttonevent":1002,"eventtype":"short_release"},{"buttonevent":1003,' \
    '"eventtype":"long_release"}]},{"repeatintervals":[800],"events":[{"buttonevent":2000,' \
    '"eventtype":"initial_press"},{"buttonevent":2001,"eventtype":"repeat"},{"buttonevent":2002,' \
    '"eventtype":"short_release"},{"buttonevent":2003,"eventtype":"long_release"}]},{"repeatintervals":[800],' \
    '"events":[{"buttonevent":3000,"eventtype":"initial_press"},{"buttonevent":3001,"eventtype":"repeat"},' \
    '{"buttonevent":3002,"eventtype":"short_release"},{"buttonevent":3003,"eventtype":"long_release"}]},' \
    '{"repeatintervals":[800],"events":[{"buttonevent":4000,"eventtype":"initial_press"},{"buttonevent":4001,' \
    '"eventtype":"repeat"},{"buttonevent":4002,"eventtype":"short_release"},{"buttonevent":4003,' \
    '"eventtype":"long_release"}]}]}},"8":{"state":{"status":0,"lastupdated":"2021-12-17T18:21:32"},"config":{' \
    '"on":true,"reachable":true},"name":"Dimmer Switch 2 SceneCycle","type":"CLIPGenericStatus","modelid":"PHWA01",' \
    '"manufacturername":"Philips","swversion":"1.0","uniqueid":"WA0001","recycle":true},"18":{"state":{"status":1,' \
    '"lastupdated":"2021-12-31T04:33:52"},"config":{"on":true,"reachable":true},"name":"cycling",' \
    '"type":"CLIPGenericStatus","modelid":"HUELABSENUM","manufacturername":"Philips","swversion":"1.0",' \
    '"uniqueid":"2:0:8f39-1b24-4981-ad24","recycle":true},"19":{"state":{"status":1,' \
    '"lastupdated":"2021-12-30T20:30:10"},"config":{"on":true,"reachable":true},"name":"cycleState",' \
    '"type":"CLIPGenericStatus","modelid":"HUELABSENUM","manufacturername":"Philips","swversion":"1.0",' \
    '"uniqueid":"0:1:c000-916a-4b5d-bf7b","recycle":true},"20":{"state":{"presence":true,' \
    '"lastupdated":"2021-12-31T04:34:08"},"swupdate":{"state":"noupdates","lastinstall":"2021-12-28T19:20:01"},' \
    '"config":{"on":true,"battery":100,"reachable":true,"alert":"none","sensitivity":2,"sensitivitymax":2,' \
    '"ledindication":false,"usertest":false,"pending":[]},"name":"Motion sensor toilet","type":"ZLLPresence",' \
    '"modelid":"SML001","manufacturername":"Signify Netherlands B.V.","productname":"Hue motion sensor",' \
    '"swversion":"6.1.1.27575","uniqueid":"00:17:88:01:0b:09:b1:e6-02-0406","capabilities":{"certified":true,' \
    '"primary":true}},"21":{"state":{"lightlevel":0,"dark":true,"daylight":false,' \
    '"lastupdated":"2021-12-31T06:03:48"},"swupdate":{"state":"noupdates","lastinstall":"2021-12-28T19:20:01"},' \
    '"config":{"on":true,"battery":100,"reachable":true,"alert":"none","tholddark":16000,"tholdoffset":7000,' \
    '"ledindication":false,"usertest":false,"pending":[]},"name":"Hue ambient light sensor 1","type":"ZLLLightLevel",' \
    '"modelid":"SML001","manufacturername":"Signify Netherlands B.V.","productname":"Hue ambient light sensor",' \
    '"swversion":"6.1.1.27575","uniqueid":"00:17:88:01:0b:09:b1:e6-02-0400","capabilities":{"certified":true,' \
    '"primary":false}},"22":{"state":{"temperature":1760,"lastupdated":"2021-12-31T06:02:58"},"swupdate":{' \
    '"state":"noupdates","lastinstall":"2021-12-28T19:20:01"},"config":{"on":true,"battery":100,"reachable":true,' \
    '"alert":"none","ledindication":false,"usertest":false,"pending":[]},"name":"Hue temperature sensor 1",' \
    '"type":"ZLLTemperature","modelid":"SML001","manufacturername":"Signify Netherlands B.V.","productname":"Hue ' \
    'temperature sensor","swversion":"6.1.1.27575","uniqueid":"00:17:88:01:0b:09:b1:e6-02-0402","capabilities":{' \
    '"certified":true,"primary":false}},"27":{"state":{"status":0,"lastupdated":"2021-12-31T04:34:08"},' \
    '"config":{"on":true,"reachable":true},"name":"presenceState","type":"CLIPGenericStatus","modelid":"HUELABSENUM",' \
    '"manufacturername":"Philips","swversion":"1.0","uniqueid":"5:12:6b53-ccd5-47e0-8fbc","recycle":true},' \
    '"28":{"state":{"status":0,"lastupdated":"2021-12-30T20:31:31"},"config":{"on":true,"reachable":true},' \
    '"name":"textState","type":"CLIPGenericStatus","modelid":"BEH_STATE","manufacturername":"Philips",' \
    '"swversion":"1.0","uniqueid":"2:13:1b24-15fa-4fac-8910","recycle":true}} '

if __name__ == '__main__':
    unittest.main()

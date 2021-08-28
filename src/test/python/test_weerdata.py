import unittest
from mock_api import MockAPI
from gateways.weer_gateway import WeerGateway
from entiteiten.weer import Weer
from device.weerhuisjenl import WeerhuisjeDevice
from device.weerlive_api import WeerLiveDevice


class MockWeerLiveDevice(WeerLiveDevice):
    def __init__(self):
        super().__init__({'weer': {'weerlive_api_key': "", 'weerlive_locatie': ""}})
        self.weer = Weer()

    def get_weerentiteit(self):
        return self.weer


class MockWeerhuisjeDevice(WeerhuisjeDevice):
    def __init__(self):
        super().__init__({'weer':{'weerhuisje_locatie_1': "weerstationwijkaanzee"}})

    def get_neerslaghoeveelheid(self):
        return 2.1


class TestWeerdata(unittest.TestCase):
    def test_weerlive_api(self):
        config = {'weer' : {'weerlive_api_key': 'demo', 'weerlive_locatie': 'IJmuiden'}}
        weerdevice = WeerLiveDevice(config)
        weerdevice.api = MockAPI()
        weerdevice.api.json = test_data_weerlive
        weer = weerdevice.extend_weerentiteit(Weer())
        self.assertEqual(weer.temperatuur, 21.5)
        self.assertEqual(weer.gevoelstemperatuur, 19.6)
        self.assertEqual(weer.windrichting, 292.5)
        self.assertEqual(weer.windsnelheidms, 4)
        self.assertEqual(weer.luchtvochtigheid, 69)
        self.assertEqual(weer.luchtdruk, 1008.9)
        for metingtype in ['temperatuur', 'gevoelstemperatuur', 'windrichting', 'windsnelheidms', 'luchtvochtigheid',
                           'luchtdruk']:
            self.assertEqual(weer.get_locatie_of_meting(metingtype), 'IJmuiden')

    def test_neerslag_api(self):
        weerdevice = WeerhuisjeDevice({'weer': {'weerhuisje_locatie_1': 'weerstationwijkaanzee'}})
        weerdevice.api = MockAPI()
        weerdevice.api.json = test_data_weerhuisje
        weer = weerdevice.extend_weerentiteit(Weer())
        self.assertEqual(weer.neerslaghoeveelheid24h, 2.1)
        self.assertEqual(weer.neerslagintensiteit, 1.0)
        for metingtype in ['neerslaghoeveelheid24h', 'neerslagintensiteit']:
            self.assertEqual(weer.get_locatie_of_meting(metingtype), 'weerstationwijkaanzee')

    def test_weer_gateway(self):
        weergateway = WeerGateway()
        weergateway.weer_devices.append(MockWeerLiveDevice())
        weergateway.weer_devices.append(MockWeerhuisjeDevice())
        weer = Weer()
        weer.temperatuur = 21.5
        weer.gevoelstemperatuur = 19.6
        weer.windrichting = "WNW"
        weer.windsnelheidms = 4
        weer.luchtvochtigheid = 69
        weer.luchtdruk = 1008.9
        weer.neerslagintensiteit = 1.0
        weer.neerslaghoeveelheid24h = 2.1
        weer._locatie = {'temperatuur': 'IJmuiden', 'gevoelstemperatuur': 'IJmuiden', 'windrichting': 'IJmuiden',
                         'windsnelheidms': 'IJmuiden', 'luchtvochtigheid': 'IJmuiden', 'luchtdruk': 'IJmuiden',
                         'neerslaghoeveelheid24h': 'weerstationwijkaanzee',
                         'neerslagintensiteit': 'weerstationwijkaanzee'}
        weergateway.weerdata = weer
        meetwaardenstr = ""
        for meetwaarde in weergateway.get_meetwaarden():
            meetwaardenstr = meetwaardenstr + " " + str(meetwaarde)
        self.assertEqual(" 21.5 gradencelsius, tags: soort=temperatuur locatie=IJmuiden"
                         " 19.6 gradencelsius, tags: soort=gevoelstemperatuur locatie=IJmuiden"
                         " 4.0 m/s, tags: soort=windsnelheid locatie=IJmuiden"
                         " 69 percentage, tags: soort=luchtvochtigheid locatie=IJmuiden"
                         " 1008.9 hPa, tags: soort=luchtdruk locatie=IJmuiden"
                         " 292.5 kompasgraden, tags: soort=windrichting locatie=IJmuiden"
                         " 2.1 mm, tags: soort=neerslaghoeveelheid locatie=weerstationwijkaanzee"
                         " 1.0 mm/h, tags: soort=neerslagintensiteit locatie=weerstationwijkaanzee"
                         , meetwaardenstr)


test_data_weerlive = \
    '{ "liveweer": [{"plaats": "IJmuiden", "temp": "21.5", "gtemp": "19.6", "samenv": "Geheel bewolkt", "lv": "69", ' \
    '"windr": "WNW", "windms": "4", "winds": "3", "windbft": "3", "windknp": "7.8", "windk": "7.8", ' \
    '"windkmh": "14.4", "luchtd": "1008.9", "ldmmhg": "757", "dauwp": "15", "zicht": "35", ' \
    '"verw": "Af en toe zon en enkele buien, vooral vandaag met onweer", "sup": "05:53", "sunder": "21:41", ' \
    '"image": "bewolkt", "d0weer": "bewolkt", "d0tmax": "23", "d0tmin": "16", "d0windk": "2", "d0windknp": "6", ' \
    '"d0windms": "3", "d0windkmh": "11", "d0windr": "Z", "d0neerslag": "8", "d0zon": "21", ' \
    '"d1weer": "halfbewolkt_regen", "d1tmax": "21", "d1tmin": "15", "d1windk": "3", "d1windknp": "8", ' \
    '"d1windms": "4", "d1windkmh": "15", "d1windr": "ZW", "d1neerslag": "70", "d1zon": "30", ' \
    '"d2weer": "halfbewolkt_regen", "d2tmax": "20", "d2tmin": "14", "d2windk": "3", "d2windknp": "8", ' \
    '"d2windms": "4", "d2windkmh": "15", "d2windr": "ZW", "d2neerslag": "40", "d2zon": "40", "wolkenbasis": "-", ' \
    '"totalebedekking": "-", "grstemp": "-", "gr": "-", "windstootms": "-", "windstootbft": "-", ' \
    '"windstootknp": "-", "windstootkmh": "-", "windrgr": "-", "alarm": "1", "alarmtxt": " Verspreid over het land ' \
    'komen enkele regen- en onweersbuien voor, lokaal met veel neerslag en kans op kleine hagel en windstoten tot ' \
    'ca. 60 km/uur. Hiervan kunnen verkeer en buitenactiviteiten hinder ondervinden. Later vanavond neemt de kans ' \
    'op onweersbuien af.  "}]}'

test_data_weerhuisje = \
    '{"date": "16:39:33", "dateFormat": "m/d/y", "temp": "20.2", "tempTL": "16.4", "tempTH": "21.4", ' \
    '"intemp": "24.2", "dew": "15.4", "dewpointTL": "6.7", "dewpointTH": "9.9", "apptemp": "24.4", ' \
    '"apptempTL": "24.4", "apptempTH": "24.4", "wchill": "21.8", "wchillTL": "4.8", "heatindex": "20.2", ' \
    '"heatindexTH": "20.2", "humidex": "24.4", "wlatest": "19.4", "wspeed": "14.8", "wgust": "21.6", ' \
    '"wgustTM": "37.1", "bearing": "248", "avgbearing": "212", "press": "998.6", "pressTL": "996.6", ' \
    '"pressTH": "1000.2", "pressL": "984.5", "pressH": "1036.3", "rfall": "2.1", "rrate": "1.0", "rrateTM": "0.8", ' \
    '"hum": "74", "humTL": "95", "humTH": "99", "inhum": "65.0", "SensorContactLost": "0", ' \
    '"forecast": "Conditions updated: 16:39:33", "tempunit": "C", "windunit": "km/h", "pressunit": "hPa", ' \
    '"rainunit": "mm", "temptrend": "0.6", "TtempTL": "05:15", "TtempTH": "11:14", "TdewpointTL": "05:03", ' \
    '"TdewpointTH": "14:11", "TapptempTL": "00:00", "TapptempTH": "00:00", "TwchillTL": "05:22", ' \
    '"TheatindexTH": "n/a", "TrrateTM": "00:00", "ThourlyrainTH": "00:00", "LastRainTipISO": "n/a", ' \
    '"hourlyrainTH": "0.0", "ThumTL": "00:00", "ThumTH": "09:00", "TpressTL": "06:00", "TpressTH": "00:00", ' \
    '"presstrendval": "0.3", "Tbeaufort": "F3", "TwgustTM": "16:06", "windTM": "37.1", "bearingTM": "212", ' \
    '"timeUTC": "2021,08,06,23,39,33", "BearingRangeFrom10": "359", "BearingRangeTo10": "0", "UV": "--", ' \
    '"UVTH": "--", "SolarRad": "--", "CurrentSolarMax": "--", "SolarTM": "90", "domwinddir": "SSW", ' \
    '"WindRoseData": "[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]", "windrun": "0.0", ' \
    '"version": "5.1", "build": "14426", "ver": "10"}'


if __name__ == '__main__':
    unittest.main()

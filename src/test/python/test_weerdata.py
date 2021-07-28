import unittest

from entiteiten.weer import Weer
from mock_api import MockAPI
from mock_weer_device import MockWeerLiveDevice
from sensor.weer_gateway import WeerGateway
from sensor.weerlive_api import WeerLiveDevice


class TestWeerdata(unittest.TestCase):
    def test_weerlive_api(self):
        config = {'weerlive' : {'api_key': 'demo', 'locatie':'IJmuiden'}}
        weerdevice = WeerLiveDevice(config)
        weerdevice.api = MockAPI()
        weerdevice.api.json = test_data
        weer = weerdevice.get_weerentiteit()
        self.assertEqual(weer.temperatuur, 21.5)
        self.assertEqual(weer.locatie, "IJmuiden")
        self.assertEqual(weer.gevoelstemperatuur, 19.6)
        self.assertEqual(weer.windrichting, 180)
        self.assertEqual(weer.windsnelheidms, 4)
        self.assertEqual(weer.luchtvochtigheid, 69)
        self.assertEqual(weer.luchtdruk, 1008.9)

    def test_weer_gateway(self):
        weergateway = WeerGateway()
        weergateway.weer_device = MockWeerLiveDevice()
        weer = Weer()
        weer.temperatuur = 21.5
        weer.locatie = "IJmuiden"
        weer.gevoelstemperatuur = 19.6
        weer.windrichting = "Zuid"
        weer.windsnelheidms = 4
        weer.luchtvochtigheid = 69
        weer.luchtdruk = 1008.9
        weergateway.weer_device.weer = weer
        meetwaardenstr = ""
        for meetwaarde in weergateway.get_meetwaarden():
            meetwaardenstr = meetwaardenstr + " " + str(meetwaarde)
        self.assertEqual(" 21.5 gradencelsius, tags: soort=temperatuur locatie=IJmuiden"
                         " 19.6 gradencelsius, tags: soort=gevoelstemperatuur locatie=IJmuiden"
                         " 4.0 m/s, tags: soort=windsnelheid locatie=IJmuiden"
                         " 69 percentage, tags: soort=luchtvochtigheid locatie=IJmuiden"
                         " 1008.9 hPa, tags: soort=luchtdruk locatie=IJmuiden"
                         " 180 graden, tags: soort=windrichting locatie=IJmuiden"
                         , meetwaardenstr)


test_data = '{ "liveweer": [{"plaats": "IJmuiden", "temp": "21.5", "gtemp": "19.6", "samenv": "Geheel bewolkt", ' \
            '"lv": "69", "windr": "Zuid", "windms": "4", "winds": "3", "windbft": "3", "windknp": "7.8", ' \
            '"windk": "7.8", "windkmh": "14.4", "luchtd": "1008.9", "ldmmhg": "757", "dauwp": "15", "zicht": "35", ' \
            '"verw": "Af en toe zon en enkele buien, vooral vandaag met onweer", "sup": "05:53", "sunder": "21:41", ' \
            '"image": "bewolkt", "d0weer": "bewolkt", "d0tmax": "23", "d0tmin": "16", "d0windk": "2", ' \
            '"d0windknp": "6", "d0windms": "3", "d0windkmh": "11", "d0windr": "Z", "d0neerslag": "8", ' \
            '"d0zon": "21", "d1weer": "halfbewolkt_regen", "d1tmax": "21", "d1tmin": "15", "d1windk": "3", ' \
            '"d1windknp": "8", "d1windms": "4", "d1windkmh": "15", "d1windr": "ZW", "d1neerslag": "70", ' \
            '"d1zon": "30", "d2weer": "halfbewolkt_regen", "d2tmax": "20", "d2tmin": "14", "d2windk": "3", ' \
            '"d2windknp": "8", "d2windms": "4", "d2windkmh": "15", "d2windr": "ZW", "d2neerslag": "40", ' \
            '"d2zon": "40", "wolkenbasis": "-", "totalebedekking": "-", "grstemp": "-", "gr": "-", ' \
            '"windstootms": "-", "windstootbft": "-", "windstootknp": "-", "windstootkmh": "-", "windrgr": "-", ' \
            '"alarm": "1", "alarmtxt": " Verspreid over het land komen enkele regen- en onweersbuien voor, lokaal ' \
            'met veel neerslag en kans op kleine hagel en windstoten tot ca. 60 km/uur. Hiervan kunnen verkeer en ' \
            'buitenactiviteiten hinder ondervinden. Later vanavond neemt de kans op onweersbuien af.  "}]}'



if __name__ == '__main__':
    unittest.main()

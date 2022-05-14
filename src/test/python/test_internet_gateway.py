import json
import time
import unittest

from device.sensor.internet_fast_com_device import FastComDevice
from device.sensor.internet_speedtest_device import SpeedtestDevice
from device.sensor.wifi_device import WifiDevice
from gateways.internet_gateway import InternetGateway


class MockSpeedtestDevice(SpeedtestDevice):
    def __init__(self, config):
        super().__init__(config)
        self._times_called = 0

    def _gettest_data(self):
        if self._testdata is None:
            self._testdata = json.loads(test_data)
            self._testdata["server"]["d"] -= self._times_called
        self._times_called += 1
        return self._testdata


class SpyWifi(WifiDevice):
    def _scan_wifi(self):
        with open("wifi_scanning.txt") as f:
            scan = f.read()
        return scan


class MockFastComDevice(FastComDevice):
    def __init__(self, config):
        super().__init__(config)

    def _get_downloadbytes_latency(self, url, token):
        time.sleep(0.1)
        return 120063, 0.03

    def _get_token(self):
        return "nnnn"

    def _get_targets(self, url, token):
        return [{'url': '1'}, {'url': '2'}, {'url': '3'}]


class InternetGatewayTest(unittest.TestCase):

    def test_get_meetwaarde(self):
        internet = InternetGateway({})
        device = MockSpeedtestDevice({'cli_path': '.'})
        device.loaded()
        internet._devices.append(device)
        device = SpyWifi({'iwlist_path': '', 'wifi_interface': '', 'wifi_id_1': 'thuis_24g',
                          'wifi_id_2': 'thuis_zolder'})
        device.loaded()
        internet._devices.append(device)
        device = MockFastComDevice({'fast_com_token_url': '.', 'fast_com_speedtest_url': '.'})
        device.loaded()
        internet._devices.append(device)
        meetwaarden = internet.get_meetwaarden()
        self.assertEqual(11, len(meetwaarden))
        meetwaarde = meetwaarden.pop(0)
        self.assertEqual(91706271.43394412, meetwaarde.waarde)
        self.assertEqual(meetwaarde.tags['naam'], 'download')
        self.assertEqual(meetwaarde.tags['server_naam'], 'Arnhem')
        self.assertEqual(meetwaarde.tags['server_afstand'], '109')
        self.assertEqual(meetwaarde.tags['client_ip'], '217.123.109.107')
        self.assertEqual(meetwaarde.tags['bron'], 'speedtest')
        meetwaarde = meetwaarden.pop(0)
        self.assertEqual(27485708.776732102, meetwaarde.waarde)
        meetwaarde = meetwaarden.pop(0)
        self.assertEqual(22.615, meetwaarde.waarde)
        meetwaarde = meetwaarden.pop(0)
        self.assertEqual((43/70)*100, meetwaarde.waarde)
        self.assertEqual(meetwaarde.tags['ssid'], 'thuis_zolder')
        self.assertEqual(meetwaarde.tags['channel'], '8')
        self.assertEqual(meetwaarde.tags['frequency'], '2.447')
        self.assertEqual(meetwaarde.tags['bron'], 'wifi')
        meetwaarde = meetwaarden.pop(0)
        self.assertEqual(-67, meetwaarde.waarde)
        meetwaarde = meetwaarden.pop(0)
        self.assertEqual(8, meetwaarde.waarde)
        meetwaarde = meetwaarden.pop(0)
        self.assertEqual((70/70)*100, meetwaarde.waarde)
        self.assertEqual(meetwaarde.tags['ssid'], 'thuis_24g')
        meetwaarden.pop(0)
        meetwaarden.pop(0)
        meetwaarde = meetwaarden.pop(0)
        self.assertEqual(9, int(meetwaarde.waarde / 1000000))
        self.assertEqual(meetwaarde.tags['naam'], 'download')
        meetwaarde = meetwaarden.pop(0)
        self.assertEqual(0.03, meetwaarde.waarde)
        self.assertEqual(meetwaarde.tags['naam'], 'ping')
        self.assertEqual(meetwaarde.tags['bron'], 'fast_com')


test_data = '{"download": 91706271.43394412, "upload": 27485708.776732102, "ping": 22.615,\
             "server": {"url": "http://speedtest.breedband.nl:8080/speedtest/upload.php", "lat": "51.9833",\
                        "lon": "5.9167",\
                        "name": "Arnhem", "country": "Netherlands", "cc": "NL", "sponsor": "Breedband", "id": "5252",\
                        "host": "speedtest.breedband.nl:8080", "d": 114.06065955630943, "latency": 22.615},\
             "timestamp": "2022-01-08T15:15:14.942401Z", "bytes_sent": 34512896, "bytes_received": 114977956,\
             "share": null,\
             "client": {"ip": "217.123.109.107", "lat": "52.4594", "lon": "4.6015", "isp": "Ziggo", "isprating": "3.7",\
                        "rating": "0", "ispdlavg": "0", "ispulavg": "0", "loggedin": "0", "country": "NL"}}'

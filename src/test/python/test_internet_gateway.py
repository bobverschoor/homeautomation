import json
import unittest

from device.speedtest import SpeedtestDevice
from gateways.internet_gateway import InternetGateway


class MockSpeedtestDevice(SpeedtestDevice):
    def __init__(self, config):
        super().__init__(config)

    def _gettest_data(self):
        if self._testdata is None:
            self._testdata = json.loads(test_data)
        return self._testdata


class TestInternetGateway(unittest.TestCase):

    def test_get_meetwaarde(self):
        internet = InternetGateway()
        internet.device = MockSpeedtestDevice({'cli_path': '.'})
        meetwaarden = internet.get_meetwaarden()
        self.assertEqual(3, len(meetwaarden))
        meetwaarde = meetwaarden.pop()
        self.assertEqual(22.615, meetwaarde.waarde)
        self.assertEqual(meetwaarde.tags['naam'], 'ping')
        self.assertEqual(meetwaarde.tags['server_id'], '5252')
        self.assertEqual(meetwaarde.tags['client_ip'], '217.123.109.107')
        meetwaarde = meetwaarden.pop()
        self.assertEqual(27485708.776732102, meetwaarde.waarde)
        meetwaarde = meetwaarden.pop()
        self.assertEqual(91706271.43394412, meetwaarde.waarde)


test_data = '{"download": 91706271.43394412, "upload": 27485708.776732102, "ping": 22.615,\
             "server": {"url": "http://speedtest.breedband.nl:8080/speedtest/upload.php", "lat": "51.9833",\
                        "lon": "5.9167",\
                        "name": "Arnhem", "country": "Netherlands", "cc": "NL", "sponsor": "Breedband", "id": "5252",\
                        "host": "speedtest.breedband.nl:8080", "d": 104.06065955630943, "latency": 22.615},\
             "timestamp": "2022-01-08T15:15:14.942401Z", "bytes_sent": 34512896, "bytes_received": 114977956,\
             "share": null,\
             "client": {"ip": "217.123.109.107", "lat": "52.4594", "lon": "4.6015", "isp": "Ziggo", "isprating": "3.7",\
                        "rating": "0", "ispdlavg": "0", "ispulavg": "0", "loggedin": "0", "country": "NL"}}'

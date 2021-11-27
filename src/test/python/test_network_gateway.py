import time
import unittest

from device.api import Api
from entiteiten.user import User
from gateways.network_gateway import NetworkGatewayException, NetworkGateway


class MockArp(Api):
    def __init__(self, url):
        super().__init__(url)
        self._scan = None

    def request_data(self):
        if self._scan is not None:
            output = {}
        else:
            output = {
                '192.168.1.1': '18:e8:29:ac:2d:77',
                '192.168.1.2': '50:d4:f7:ba:c8:06',
                '192.168.1.3': '60:a4:4c:a0:d8:e0',
                '192.168.1.15': 'dc:56:e7:4e:b5:7a',
                '192.168.1.17': 'b8:27:eb:41:5b:45',
                '192.168.1.20': '00:11:32:5b:95:5f',
                '192.168.1.31': '78:c8:81:eb:33:da',
                '192.168.1.53': 'b8:27:eb:8b:df:9b',
                '192.168.1.60': 'ec:b5:fa:06:0d:12',
                '192.168.1.41': 'f8:0d:60:54:46:7a',
                '192.168.1.142': '00:e0:4c:7f:b4:c5',
                '192.168.1.30': '98:b6:e9:cd:08:e9',
                '192.168.1.104': 'f0:18:98:0a:0b:0e',
                '192.168.1.124': '9e:66:4a:a7:91:60',
                '192.168.1.139': 'fa:0f:fe:34:7f:ee',
                '192.168.1.141': '4c:32:75:91:9f:6b',
                '192.168.1.147': '22:c5:a4:be:ec:8c'}
        self._scan = {}
        for key in output.keys():
            self._scan[output[key]] = key

    def get_json(self):
        return self._scan


class NetworkGatewayTest(unittest.TestCase):
    def test_init(self):
        self.assertRaises(NetworkGatewayException, NetworkGateway, {}, [])
        network = NetworkGateway({NetworkGateway.CONFIG_NETWORK: {'local_ip_range': 'test'}}, [])
        self.assertEqual(network._local_ip_range, 'test')

    def test_is_reachable(self):
        network = NetworkGateway({NetworkGateway.CONFIG_NETWORK: {'local_ip_range': 'test', 'cache_ttl': 0.1}}, [])
        mock_arp = MockArp('test')
        network.set_network_device(mock_arp)
        self.assertTrue(network.is_reachable('22:c5:a4:be:ec:8c'))
        self.assertTrue(network.is_reachable('22c5a4beec8c'))
        self.assertFalse(network.is_reachable('22c5a4beec8d'))
        time.sleep(0.1)
        self.assertFalse(network.is_reachable('22c5a4beec8c'))

    def test_get_meetwaarden(self):
        users = [User({'chat_id': '', 'username': 'Bob', 'mac_addresses': '4e:fb:6b:ff:ec:96, 22:c5:a4:be:ec:8c'})]
        network = NetworkGateway({NetworkGateway.CONFIG_NETWORK: {'local_ip_range': 'test', 'cache_ttl': 0.1}}, users)
        mock_arp = MockArp('test')
        network.set_network_device(mock_arp)
        meetwaarde = network.get_meetwaarden().pop()
        self.assertTrue(meetwaarde.waarde)
        self.assertEqual({'naam': 'Bob'}, meetwaarde.tags)

    def test_get_meetwaarden_with_api_unavailable(self):
        users = [User({'chat_id': '', 'username': 'Bob', 'mac_addresses': '4e:fb:6b:ff:ec:96, 22:c5:a4:be:ec:8c'})]
        network = NetworkGateway({NetworkGateway.CONFIG_NETWORK: {'local_ip_range': 'test', 'cache_ttl': 0.1}}, users)
        network.set_network_device(Api('http://127.0.0.1:8000'))
        meetwaarde = network.get_meetwaarden().pop()
        self.assertFalse(meetwaarde.waarde)


if __name__ == '__main__':
    unittest.main()

from datetime import datetime, timedelta

from device.api import ApiException
from entiteiten.meetwaarde import Meetwaarde


class NetworkGatewayException(Exception):
    def __init__(self, message):
        super(NetworkGatewayException, self).__init__(message)


def scan_cache_is_old(last_scan_datetime, cachettl):
    if last_scan_datetime:
        if last_scan_datetime > datetime.now() - timedelta(seconds=cachettl):
            return False
    return True


class NetworkGateway:
    CONFIG_NETWORK = 'network'
    CONFIG_LOCAL_IP_RANGE = 'local_ip_range'
    DEFAULT_LOCAL_IP_RANGE = '192.168.1.0/24'
    CONFIG_DATABASENAAM = 'databasenaam'
    CONFIG_CACHE_TTL = 'cache_ttl'
    DEFAULT_CACHE_TTL = 120

    def __init__(self, config, users, debug=False):
        self._debug = debug
        if NetworkGateway.CONFIG_NETWORK in config:
            self._config = config[NetworkGateway.CONFIG_NETWORK]
            if NetworkGateway.CONFIG_LOCAL_IP_RANGE in self._config:
                self._local_ip_range = self._config[NetworkGateway.CONFIG_LOCAL_IP_RANGE]
            else:
                self._local_ip_range = NetworkGateway.DEFAULT_LOCAL_IP_RANGE
            if NetworkGateway.CONFIG_CACHE_TTL in self._config:
                self._cache_ttl = self._config[NetworkGateway.CONFIG_CACHE_TTL]
            else:
                self._cache_ttl = NetworkGateway.DEFAULT_CACHE_TTL
        else:
            raise NetworkGatewayException("Config missing network section")
        self._users = users
        self._network_device = None
        self._scan = None
        self._last_scan_datetime = None

    def set_network_device(self, network):
        self._network_device = network

    def is_reachable(self, mac_address):
        if self._network_device is None:
            raise NetworkGatewayException("network device not set")
        if scan_cache_is_old(self._last_scan_datetime, self._cache_ttl):
            try:
                self._network_device.request_data()
                self._scan = self._network_device.get_json()
            except ApiException as e:
                print("API not available\n" + str(e))
                self._scan = {}
            self._last_scan_datetime = datetime.now()
        for active_mac in self._scan.keys():
            active_mac = active_mac.replace(' ', '').replace(':', '').lower()
            mac_address = mac_address.replace(' ', '').replace(':', '').lower()
            if mac_address == active_mac:
                return True
        return False

    def get_meetwaarden(self):
        meetwaarden = []
        if self._network_device is None:
            raise ModuleNotFoundError("Network device not set")
        for user in self._users:
            meetwaarde = Meetwaarde('aanwezig')
            meetwaarde.timestamp = datetime.now()
            meetwaarde.tags = "naam:" + user.name
            meetwaarde.waarde = False
            for mac_address in user.macadresses:
                if self.is_reachable(mac_address):
                    meetwaarde.waarde = True
                    continue
            meetwaarden.append(meetwaarde)
        return meetwaarden

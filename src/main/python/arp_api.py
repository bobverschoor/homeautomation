import configparser
import os

from fastapi import FastAPI
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


class ArpException(Exception):
    def __init__(self, message):
        super(ArpException, self).__init__(message)


class Arp:
    CONFIG_ARP = 'arp'
    CONFIG_LOCAL_IP_RANGE = 'local_ip_range'
    DEFAULT_LOCAL_IP_RANGE = '192.168.1.0/24'
    DEFAULT_BROADCAST = "ff:ff:ff:ff:ff:ff"
    CONFIG_DATABASENAAM = 'databasenaam'
    CONFIG_CACHE_TTL = 'cache_ttl'
    DEFAULT_CACHE_TTL = 120

    def __init__(self, configfile):
        self._config = configparser.ConfigParser()
        if os.path.exists(configfile):
            self._config.read(configfile)
            if Arp.CONFIG_ARP in self._config:
                self._config = self._config[Arp.CONFIG_ARP]
                if Arp.CONFIG_LOCAL_IP_RANGE in self._config:
                    self._local_ip_range = self._config[Arp.CONFIG_LOCAL_IP_RANGE]
                else:
                    self._local_ip_range = Arp.DEFAULT_LOCAL_IP_RANGE
                if Arp.CONFIG_CACHE_TTL in self._config:
                    self._cache_ttl = self._config[Arp.CONFIG_CACHE_TTL]
                else:
                    self._cache_ttl = Arp.DEFAULT_CACHE_TTL
            else:
                raise ArpException("Config missing network section")
        self.broadcast_address = Arp.DEFAULT_BROADCAST
        self.routeraddress = "192.168.1.1"

    def get_active_local_mac_ip_addresses(self):
        import scapy.all
        from scapy.layers.l2 import Ether, ARP
        ans, unans = scapy.all.srp(Ether(dst=self.broadcast_address) / ARP(pdst=self._local_ip_range, ),
                                   timeout=15, verbose=0, iface='eth0')
        found_mac = {}
        for snd, rcv in ans:
            if rcv is not None:
                for element in rcv:
                    found_mac[str(element.hwsrc)] = str(element.psrc)
        return found_mac


if __name__ == "__main__":
    app = FastAPI()
    arp = Arp('src/main/resources/secrets.ini')


    @app.get("/")
    async def root():
        return arp.get_active_local_mac_ip_addresses()

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


class Arp:
    def __init__(self, local_ip_range):
        self.interface = '192.168.1.0/24'
        self.broadcast_address = "ff:ff:ff:ff:ff:ff"

    def get_active_local_mac_ip_addresses(self):
        import scapy.all
        from scapy.layers.l2 import Ether, ARP
        ans, unans = scapy.all.srp(Ether(dst=self.broadcast_address) / ARP(pdst=self.interface), timeout=2)
        found_mac = {}
        for snd, rcv in ans:
            if rcv is not None:
                for element in rcv:
                    found_mac[str(element.hwsrc)] = str(element.psrc)
        return found_mac

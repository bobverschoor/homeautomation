from phue import Bridge


class HueBridgeDevice:

    def __init__(self, ip_adres = "192.168.1.44"):
        self.bridge_ip = ip_adres
        self.bridge = Bridge(self.bridge_ip)

    def get_entities(self):
        return self.bridge

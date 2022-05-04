from device.sensor.internet_fast_com_device import FastComDevice
from device.sensor.internet_speedtest_device import SpeedtestDeviceException, SpeedtestDevice
from device.sensor.wifi_device import WifiDevice
from entiteiten.meetwaarde import Meetwaarde, convertlist2tags


class InternetGateway:
    def __init__(self, config):
        self._config = config
        self._devices = []

    def load_devices(self):
        device = SpeedtestDevice(self._config)
        if device.loaded():
            self._devices.append(device)
        else:
            print("SpeedtestDevice not loaded")
        device = WifiDevice(self._config)
        if device.loaded():
            self._devices.append(device)
        else:
            print("WifiDevice is not loaded")
        device = FastComDevice(self._config)
        if device.loaded():
            self._devices.append(device)
        else:
            print("FastComDevice is not loaded")

    def get_meetwaarden(self):
        meetwaarden = []
        if not self._devices:
            raise ModuleNotFoundError("Device not set")
        try:
            for device in self._devices:
                if device.type == "speedtest":
                    meetwaarden.extend(get_speedtest_meetwaarden(device))
                elif device.type == "wifi":
                    meetwaarden.extend(get_wifi_meetwaarden(device))
                elif device.type == "fast_com":
                    meetwaarden.extend(get_fastcom_meetwaarden(device))
        except SpeedtestDeviceException:
            print("Geen meetwaarden")
        return meetwaarden


def get_speedtest_tags(device, name):
    return ["naam:" + name, "bron:" + device.type,
            "client_ip:" + device.get_client_ip(), "server_naam:" + device.get_server_name(),
            "server_afstand:" + str(device.get_server_distance())]


def get_wifi_tags(netwerk, bron):
    return ["ssid:" + netwerk.essid, "channel:" + str(netwerk.channel), "frequency:" + str(netwerk.frequency_ghz),
            "bron:" + bron]


def get_speedtest_meetwaarden(device):
    meetwaarden = [Meetwaarde(eenheid='snelheid_bit_s', waarde=device.get_download_speed(),
                              tags=convertlist2tags(get_speedtest_tags(device, 'download'))),
                   Meetwaarde(eenheid='snelheid_bit_s', waarde=device.get_upload_speed(),
                              tags=convertlist2tags(get_speedtest_tags(device, 'upload'))),
                   Meetwaarde(eenheid='latentie_ms', waarde=device.get_ping_speed(),
                              tags=convertlist2tags(get_speedtest_tags(device, 'ping')))]
    return meetwaarden


def get_wifi_meetwaarden(device):
    meetwaarden = []
    for netwerk in device.get_netwerken():
        meetwaarden.append(Meetwaarde(eenheid='kwaliteit_percentage', waarde=netwerk.quality_percentage,
                                      tags=convertlist2tags(get_wifi_tags(netwerk, device.type))))
        meetwaarden.append(Meetwaarde(eenheid='signallevel_dbm', waarde=netwerk.signallevel_dbm,
                                      tags=convertlist2tags(get_wifi_tags(netwerk, device.type))))
        meetwaarden.append(Meetwaarde(eenheid='kanaal', waarde=netwerk.channel,
                                      tags=convertlist2tags(get_wifi_tags(netwerk, device.type))))
    return meetwaarden


def get_fastcom_meetwaarden(device):
    meetwaarden = [Meetwaarde(eenheid='snelheid_bit_s', waarde=device.get_download_speed(),
                              tags=convertlist2tags(["naam:download", "bron:" + device.type])),
                   Meetwaarde(eenheid='latentie_ms', waarde=device.get_ping_speed(),
                              tags=convertlist2tags(["naam:ping", "bron:" + device.type]))]
    return meetwaarden

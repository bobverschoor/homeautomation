from device.fast_com import FastComDevice
from device.speedtest import SpeedtestDeviceException, SpeedtestDevice
from device.wifi_device import WifiDevice
from entiteiten.meetwaarde import Meetwaarde


class InternetGateway:
    def __init__(self, config):
        self._config = config
        self._devices = []

    def load_devices(self):
        device = SpeedtestDevice(self._config['internet'])
        if device.loaded():
            self._devices.append(device)
        device = WifiDevice(self._config['internet'])
        if device.loaded():
            self._devices.append(device)
        device = FastComDevice(self._config['internet'])
        if device.loaded():
            self._devices.append(device)

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
    return ["naam:" + name, "server_id:" + str(device.get_server_id()),
            "client_ip:" + device.get_client_ip(), "server_naam:" + device.get_server_name(),
            "server_afstand:" + str(device.get_server_distance())]


def get_wifi_tags(netwerk):
    return ["ssid:" + netwerk.essid, "channel:" + str(netwerk.channel), "frequency:" + str(netwerk.frequency_ghz)]


def get_speedtest_meetwaarden(device):
    meetwaarden = []
    meetwaarde = Meetwaarde('snelheid_bit_s')
    meetwaarde.waarde = device.get_download_speed()
    meetwaarde.tags = get_speedtest_tags(device, 'download')
    meetwaarden.append(meetwaarde)
    meetwaarde = Meetwaarde('snelheid_bit_s')
    meetwaarde.waarde = device.get_upload_speed()
    meetwaarde.tags = get_speedtest_tags(device, 'upload')
    meetwaarden.append(meetwaarde)
    meetwaarde = Meetwaarde('latentie_ms')
    meetwaarde.waarde = device.get_ping_speed()
    meetwaarde.tags = get_speedtest_tags(device, 'ping')
    meetwaarden.append(meetwaarde)
    return meetwaarden


def get_wifi_meetwaarden(device):
    meetwaarden = []
    for netwerk in device.get_netwerken():
        meetwaarde = Meetwaarde('kwaliteit_percentage')
        meetwaarde.waarde = netwerk.quality_percentage
        meetwaarde.tags = get_wifi_tags(netwerk)
        meetwaarden.append(meetwaarde)
        meetwaarde = Meetwaarde('signallevel_dbm')
        meetwaarde.waarde = netwerk.signallevel_dbm
        meetwaarde.tags = get_wifi_tags(netwerk)
        meetwaarden.append(meetwaarde)
        meetwaarde = Meetwaarde('kanaal')
        meetwaarde.waarde = netwerk.channel
        meetwaarde.tags = get_wifi_tags(netwerk)
        meetwaarden.append(meetwaarde)
    return meetwaarden


def get_fastcom_meetwaarden(device):
    meetwaarden = []
    meetwaarde = Meetwaarde('snelheid_bit_s')
    meetwaarde.waarde = device.get_download_speed()
    meetwaarde.tags = "naam:download"
    meetwaarden.append(meetwaarde)
    meetwaarde = Meetwaarde('latentie_ms')
    meetwaarde.waarde = device.get_ping_speed()
    meetwaarde.tags = "naam:ping"
    meetwaarden.append(meetwaarde)
    return meetwaarden

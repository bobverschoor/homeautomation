from device.speedtest import SpeedtestDeviceException
from entiteiten.meetwaarde import Meetwaarde


class InternetGateway:
    def __init__(self):
        self.devices = []

    def get_meetwaarden(self):
        meetwaarden = []
        if not self.devices:
            raise ModuleNotFoundError("Device not set")
        try:
            for device in self.devices:
                if device.type == "speedtest":
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
                elif device.type == "wifi":
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
        except SpeedtestDeviceException:
            print("Geen meetwaarden")
        return meetwaarden


def get_speedtest_tags(device, name):
    return ["naam:" + name, "server_id:" + str(device.get_server_id()),
            "client_ip:" + device.get_client_ip(), "server_naam:" + device.get_server_name(),
            "server_afstand:" + str(device.get_server_distance())]


def get_wifi_tags(netwerk):
    return ["ssid:" + netwerk.essid, "channel:" + str(netwerk.channel), "frequency:" + str(netwerk.frequency_ghz)]
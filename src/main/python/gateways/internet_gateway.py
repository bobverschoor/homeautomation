from entiteiten.meetwaarde import Meetwaarde


class InternetGateway:
    def __init__(self):
        self.device = None

    def get_meetwaarden(self):
        meetwaarden = []
        if self.device is None:
            raise ModuleNotFoundError("Device not set")
        meetwaarde = Meetwaarde('snelheid_bit_s')
        meetwaarde.waarde = self.device.get_download_speed()
        meetwaarde.tags = self._get_tags('download')
        meetwaarden.append(meetwaarde)
        meetwaarde = Meetwaarde('snelheid_bit_s')
        meetwaarde.waarde = self.device.get_upload_speed()
        meetwaarde.tags = self._get_tags('upload')
        meetwaarden.append(meetwaarde)
        meetwaarde = Meetwaarde('latentie_ms')
        meetwaarde.waarde = self.device.get_ping_speed()
        meetwaarde.tags = self._get_tags('ping')
        meetwaarden.append(meetwaarde)
        return meetwaarden

    def _get_tags(self, name):
        return ["naam:" + name, "server_id:" + str(self.device.get_server_id()),
                "client_ip:" + self.device.get_client_ip(), "server_naam:" + self.device.get_server_name(),
                "server_afstand:" + str(self.device.get_server_distance())]
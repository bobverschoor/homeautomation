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
        meetwaarde.tags = "naam:download"
        meetwaarde.tags = "server_id:" + self.device.get_server_id()
        meetwaarde.tags = "client_ip:" + self.device.get_client_ip()
        meetwaarden.append(meetwaarde)
        meetwaarde = Meetwaarde('snelheid_bit_s')
        meetwaarde.waarde = self.device.get_upload_speed()
        meetwaarde.tags = "naam:upload"
        meetwaarde.tags = "server_id:" + self.device.get_server_id()
        meetwaarde.tags = "client_ip:" + self.device.get_client_ip()
        meetwaarden.append(meetwaarde)
        meetwaarde = Meetwaarde('latentie_ms')
        meetwaarde.waarde = self.device.get_ping_speed()
        meetwaarde.tags = "naam:ping"
        meetwaarde.tags = "server_id:" + self.device.get_server_id()
        meetwaarde.tags = "client_ip:" + self.device.get_client_ip()
        meetwaarden.append(meetwaarde)
        return meetwaarden

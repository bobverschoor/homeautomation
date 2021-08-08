from entiteiten.meetwaarde import Meetwaarde
from entiteiten.weer import Weer


class WeerGateway:
    def __init__(self):
        self.weer_device = None
        self.neerslag_device = None
        self.weer_devices = []
        self.weerdata = None

    def get_weerdata(self):
        self.weerdata = Weer()
        if not self.weer_devices:
            raise ModuleNotFoundError("weer device not set")
        for weerdevice in self.weer_devices:
            self.weerdata = weerdevice.extend_weerentiteit(self.weerdata)

    def get_meetwaarden(self):
        meetwaarden = []
        if not self.weerdata:
            self.get_weerdata()
        if self.weerdata.error != "":
            print("Fout bij ophalen weer gegevens: " + self.weerdata.error)
        else:
            for property_name, value in self.weerdata.get_properties():
                if property_name == "temperatuur":
                    meetwaarde = Meetwaarde("gradencelsius")
                    meetwaarde.waarde = value
                    meetwaarde.tags = "soort:temperatuur"
                    meetwaarde.tags = "locatie:" + self.weerdata.get_locatie_of_meting(property_name)
                elif property_name == "gevoelstemperatuur":
                    meetwaarde = Meetwaarde("gradencelsius")
                    meetwaarde.waarde = value
                    meetwaarde.tags = "soort:gevoelstemperatuur"
                    meetwaarde.tags = "locatie:" + self.weerdata.get_locatie_of_meting(property_name)
                elif property_name == "windsnelheidms":
                    meetwaarde = Meetwaarde("m/s")
                    meetwaarde.waarde = value
                    meetwaarde.tags = "soort:windsnelheid"
                    meetwaarde.tags = "locatie:" + self.weerdata.get_locatie_of_meting(property_name)
                elif property_name == "luchtvochtigheid":
                    meetwaarde = Meetwaarde("percentage")
                    meetwaarde.waarde = value
                    meetwaarde.tags = "soort:luchtvochtigheid"
                    meetwaarde.tags = "locatie:" + self.weerdata.get_locatie_of_meting(property_name)
                elif property_name == "luchtdruk":
                    meetwaarde = Meetwaarde("hPa")
                    meetwaarde.waarde = value
                    meetwaarde.tags = "soort:luchtdruk"
                    meetwaarde.tags = "locatie:" + self.weerdata.get_locatie_of_meting(property_name)
                elif property_name == "windrichting":
                    meetwaarde = Meetwaarde("kompasgraden")
                    meetwaarde.waarde = value
                    meetwaarde.tags = "soort:windrichting"
                    meetwaarde.tags = "locatie:" + self.weerdata.get_locatie_of_meting(property_name)
                elif property_name == "neerslaghoeveelheid24h":
                    meetwaarde = Meetwaarde("mm")
                    meetwaarde.waarde = value
                    meetwaarde.tags = "soort:neerslaghoeveelheid"
                    meetwaarde.tags = "locatie:" + self.weerdata.get_locatie_of_meting(property_name)
                elif property_name == "neerslagintensiteit":
                    meetwaarde = Meetwaarde("mm/h")
                    meetwaarde.waarde = value
                    meetwaarde.tags = "soort:neerslagintensiteit"
                    meetwaarde.tags = "locatie:" + self.weerdata.get_locatie_of_meting(property_name)
                else:
                    meetwaarde = None
                if meetwaarde:
                    meetwaarden.append(meetwaarde)
        return meetwaarden

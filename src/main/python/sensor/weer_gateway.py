from entiteiten.meetwaarde import Meetwaarde


class WeerGateway:
    def __init__(self):
        self.weer_device = None

    def get_meetwaarden(self):
        meetwaarden = []
        if self.weer_device is None:
            raise ModuleNotFoundError("weer device not set")
        weerdata = self.weer_device.get_weerentiteit()
        if weerdata.error != "":
            print("Fout bij weer: " + weerdata.error)
        else:
            for property_name, value in weerdata.get_properties():
                if property_name == "temperatuur":
                    meetwaarde = Meetwaarde("gradencelsius")
                    meetwaarde.waarde = value
                    meetwaarde.tags = "soort:temperatuur"
                    meetwaarde.tags = "locatie:" + weerdata.locatie
                elif property_name == "gevoelstemperatuur":
                    meetwaarde = Meetwaarde("gradencelsius")
                    meetwaarde.waarde = value
                    meetwaarde.tags = "soort:gevoelstemperatuur"
                    meetwaarde.tags = "locatie:" + weerdata.locatie
                elif property_name == "windsnelheidms":
                    meetwaarde = Meetwaarde("m/s")
                    meetwaarde.waarde = value
                    meetwaarde.tags = "soort:windsnelheid"
                    meetwaarde.tags = "locatie:" + weerdata.locatie
                elif property_name == "luchtvochtigheid":
                    meetwaarde = Meetwaarde("percentage")
                    meetwaarde.waarde = value
                    meetwaarde.tags = "soort:luchtvochtigheid"
                    meetwaarde.tags = "locatie:" + weerdata.locatie
                elif property_name == "luchtdruk":
                    meetwaarde = Meetwaarde("hPa")
                    meetwaarde.waarde = value
                    meetwaarde.tags = "soort:luchtdruk"
                    meetwaarde.tags = "locatie:" + weerdata.locatie
                elif property_name == "windrichting":
                    meetwaarde = Meetwaarde("graden")
                    meetwaarde.waarde = value
                    meetwaarde.tags = "soort:windrichting"
                    meetwaarde.tags = "locatie:" + weerdata.locatie
                else:
                    meetwaarde = None
                if meetwaarde is not None:
                    meetwaarden.append(meetwaarde)
        return meetwaarden


from entiteiten.meetwaarde import Meetwaarde, convert2tags
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
                    meetwaarde = Meetwaarde(eenheid="gradencelsius", waarde=value, tags=convert2tags(
                        ["soort:temperatuur", "locatie:" + self.weerdata.get_locatie_of_meting(property_name)]
                    ))
                elif property_name == "gevoelstemperatuur":
                    meetwaarde = Meetwaarde(eenheid="gradencelsius", waarde=value, tags=convert2tags(
                        ["soort:gevoelstemperatuur", "locatie:" + self.weerdata.get_locatie_of_meting(property_name)]
                    ))
                elif property_name == "windsnelheidms":
                    meetwaarde = Meetwaarde(eenheid="m/s", waarde=value, tags=convert2tags(
                        ["soort:windsnelheid", "locatie:" + self.weerdata.get_locatie_of_meting(property_name)]
                    ))
                elif property_name == "luchtvochtigheid":
                    meetwaarde = Meetwaarde(eenheid="percentage", waarde=value, tags=convert2tags(
                        ["soort:luchtvochtigheid", "locatie:" + self.weerdata.get_locatie_of_meting(property_name)]
                    ))
                elif property_name == "luchtdruk":
                    meetwaarde = Meetwaarde(eenheid="hPa", waarde=value, tags=convert2tags(
                        ["soort:luchtdruk", "locatie:" + self.weerdata.get_locatie_of_meting(property_name)]
                    ))
                elif property_name == "windrichting":
                    meetwaarde = Meetwaarde(eenheid="kompasgraden", waarde=value, tags=convert2tags(
                        ["soort:windrichting", "locatie:" + self.weerdata.get_locatie_of_meting(property_name)]
                    ))
                elif property_name == "neerslaghoeveelheid24h":
                    meetwaarde = Meetwaarde(eenheid="mm", waarde=value, tags=convert2tags(
                        ["soort:neerslaghoeveelheid", "locatie:" + self.weerdata.get_locatie_of_meting(property_name)]
                    ))
                elif property_name == "neerslagintensiteit":
                    meetwaarde = Meetwaarde(eenheid="mm/h", waarde=value, tags=convert2tags(
                        ["soort:neerslagintensiteit", "locatie:" + self.weerdata.get_locatie_of_meting(property_name)]
                    ))
                else:
                    meetwaarde = None
                if meetwaarde:
                    meetwaarden.append(meetwaarde)
        return meetwaarden

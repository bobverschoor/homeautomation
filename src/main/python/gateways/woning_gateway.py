import re

from entiteiten.meetwaarde import Meetwaarde
from entiteiten.sensor import Schakelaar, BewegingSchakelaar, TemperatuurSensor, LichtSensor


class WoningGateway:

    def __init__(self):
        self.bridge = None

    def get_meetwaarden(self):
        meetwaarden = []
        if self.bridge is None:
            raise ModuleNotFoundError("Bridge device not set")
        meetwaarden.extend(self._get_meetwaarden_lichten())
        meetwaarden.extend(self._get_meetwaarden_sensoren())
        return meetwaarden

    def alarmeer_lichten_in_groep(self):
        if self.bridge is None:
            raise ModuleNotFoundError("Bridge device not set")
        lights2alert = []
        for licht in self.bridge.get_alle_lichten_in_alarmeergroep():
            lights2alert.append(licht)
        self.bridge.alert_lights(lights2alert)

    def _get_meetwaarden_lichten(self):
        meetwaarden = []
        for licht in self.bridge.get_alle_lichten():
            meetwaarde = Meetwaarde('licht_aan')
            meetwaarde.waarde = licht.aan
            meetwaarde.tags = set_naam_id(licht.naam, licht.unique_id)
            meetwaarden.append(meetwaarde)
            meetwaarde = Meetwaarde('bereikbaar')
            meetwaarde.waarde = licht.bereikbaar
            meetwaarde.tags = set_naam_id(licht.naam, licht.unique_id)
            meetwaarden.append(meetwaarde)
        return meetwaarden

    def _get_meetwaarden_sensoren(self):
        meetwaarden = []
        for sensor in self.bridge.get_alle_sensors():
            meetwaarde = Meetwaarde('batterijpercentage')
            meetwaarde.waarde = sensor.batterijpercentage
            meetwaarde.tags = set_naam_id(sensor.naam, sensor.unique_id)
            meetwaarden.append(meetwaarde)
            meetwaarde = Meetwaarde('bereikbaar')
            meetwaarde.waarde = sensor.bereikbaar
            meetwaarde.tags = set_naam_id(sensor.naam, sensor.unique_id)
            meetwaarden.append(meetwaarde)
            if isinstance(sensor, Schakelaar):
                meetwaarde = Meetwaarde('knop_event')
                meetwaarde.waarde = sensor.knop_event
                meetwaarde.tags = set_naam_id(sensor.naam, sensor.unique_id)
                meetwaarden.append(meetwaarde)
            if isinstance(sensor, BewegingSchakelaar):
                meetwaarde = Meetwaarde('aanwezigheid')
                meetwaarde.waarde = sensor.beweging_gesignaleerd
                meetwaarde.tags = set_naam_id(sensor.naam, sensor.unique_id)
                meetwaarden.append(meetwaarde)
            if isinstance(sensor, TemperatuurSensor):
                meetwaarde = Meetwaarde('temperatuur_celsius')
                meetwaarde.waarde = sensor.temperature_celsius
                meetwaarde.tags = set_naam_id(sensor.naam, sensor.unique_id)
                meetwaarden.append(meetwaarde)
            if isinstance(sensor, LichtSensor):
                meetwaarde = Meetwaarde('lichtwaarde_lux')
                meetwaarde.waarde = sensor.lichtniveau_lux
                meetwaarde.tags = set_naam_id(sensor.naam, sensor.unique_id)
                meetwaarden.append(meetwaarde)


        return meetwaarden


def non_alphanumeric_chars(input):
    output = re.sub(r'\W+', '', input)
    return output


def set_naam_id(naam, unique_id):
    return ["naam:" + naam, "id:" + non_alphanumeric_chars(unique_id)]


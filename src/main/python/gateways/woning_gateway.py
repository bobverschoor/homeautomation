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
            meetwaarden.append(meetwaarde(naam='licht_aan', waarde=licht.aan,
                                          tags=set_naam_id(licht.naam, licht.unique_id)))
            meetwaarden.append(meetwaarde(naam='bereikbaar', waarde=licht.bereikbaar,
                                          tags=set_naam_id(licht.naam, licht.unique_id)))
        return meetwaarden

    def _get_meetwaarden_sensoren(self):
        meetwaarden = []
        for sensor in self.bridge.get_alle_sensors():
            meetwaarden.append(meetwaarde(naam='batterijpercentage', waarde=sensor.batterijpercentage,
                                          tags=set_naam_id(sensor.naam, sensor.unique_id)))
            meetwaarden.append(meetwaarde(naam='bereikbaar', waarde=sensor.bereikbaar,
                                          tags=set_naam_id(sensor.naam, sensor.unique_id)))
            if isinstance(sensor, Schakelaar):
                meetwaarden.append(meetwaarde(naam='knop_event', waarde=sensor.knop_event,
                                              tags=set_naam_id(sensor.naam, sensor.unique_id)))
            if isinstance(sensor, BewegingSchakelaar):
                meetwaarden.append(meetwaarde(naam='aanwezigheid', waarde=sensor.beweging_gesignaleerd,
                                              tags=set_naam_id(sensor.naam, sensor.unique_id)))
            if isinstance(sensor, TemperatuurSensor):
                meetwaarden.append(meetwaarde(naam='temperatuur_celsius', waarde=sensor.temperature_celsius,
                                              tags=set_naam_id(sensor.naam, sensor.unique_id)))
            if isinstance(sensor, LichtSensor):
                meetwaarden.append(meetwaarde(naam='lichtwaarde_lux', waarde=sensor.lichtniveau_lux,
                                              tags=set_naam_id(sensor.naam, sensor.unique_id)))
        return meetwaarden


def non_alphanumeric_chars(inputvalue):
    output = re.sub(r'\W+', '', inputvalue)
    return output


def set_naam_id(naam, unique_id):
    return ["naam:" + naam, "id:" + non_alphanumeric_chars(unique_id)]


def meetwaarde(naam="", waarde=0, tags=None):
    if tags is None:
        tags = []
    mw = Meetwaarde(naam)
    mw.waarde = waarde
    mw.tags = tags
    return mw

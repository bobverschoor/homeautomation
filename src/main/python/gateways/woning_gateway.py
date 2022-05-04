import re

from entiteiten.meetwaarde import Meetwaarde, convertlist2tags
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
            meetwaarden.append(Meetwaarde(eenheid='licht_aan', waarde=licht.aan,
                                          tags=convertlist2tags(set_naam_id(licht.naam, licht.unique_id))))
            meetwaarden.append(Meetwaarde(eenheid='bereikbaar', waarde=licht.bereikbaar,
                                          tags=convertlist2tags(set_naam_id(licht.naam, licht.unique_id))))
        return meetwaarden

    def _get_meetwaarden_sensoren(self):
        meetwaarden = []
        for sensor in self.bridge.get_alle_sensors():
            meetwaarden.append(Meetwaarde(eenheid='batterijpercentage', waarde=sensor.batterijpercentage,
                                          tags=convertlist2tags(set_naam_id(sensor.naam, sensor.unique_id))))
            meetwaarden.append(Meetwaarde(eenheid='bereikbaar', waarde=sensor.bereikbaar,
                                          tags=convertlist2tags(set_naam_id(sensor.naam, sensor.unique_id))))
            if isinstance(sensor, Schakelaar):
                meetwaarden.append(Meetwaarde(eenheid='knop_event', waarde=sensor.knop_event,
                                              tags=convertlist2tags(set_naam_id(sensor.naam, sensor.unique_id))))
            if isinstance(sensor, BewegingSchakelaar):
                meetwaarden.append(Meetwaarde(eenheid='aanwezigheid', waarde=sensor.beweging_gesignaleerd,
                                              tags=convertlist2tags(set_naam_id(sensor.naam, sensor.unique_id))))
            if isinstance(sensor, TemperatuurSensor):
                meetwaarden.append(Meetwaarde(eenheid='temperatuur_celsius', waarde=sensor.temperature_celsius,
                                              tags=convertlist2tags(set_naam_id(sensor.naam, sensor.unique_id))))
            if isinstance(sensor, LichtSensor):
                meetwaarden.append(Meetwaarde(eenheid='lichtwaarde_lux', waarde=sensor.lichtniveau_lux,
                                              tags=convertlist2tags(set_naam_id(sensor.naam, sensor.unique_id))))
        return meetwaarden


def non_alphanumeric_chars(inputvalue):
    output = re.sub(r'\W+', '', inputvalue)
    return output


def set_naam_id(naam, unique_id):
    return ["naam:" + naam, "id:" + non_alphanumeric_chars(unique_id)]

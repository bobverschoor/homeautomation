import datetime
import math

class SensorException(Exception):
    def __init__(self, message):
        super(SensorException, self).__init__(message)


class Sensor:
    def __init__(self, volgnr):
        self._volgr = volgnr
        self._naam = ""
        self._unique_id = ""
        self._bereikbaar = False
        self._batterijpercentage = -1
        self._tijdstip_meting = datetime.datetime.now()

    @property
    def naam(self):
        return self._naam

    @naam.setter
    def naam(self, value):
        self._naam = value

    @property
    def unique_id(self):
        return self._unique_id

    @unique_id.setter
    def unique_id(self, value):
        self._unique_id = value

    @property
    def bereikbaar(self):
        return self._bereikbaar

    @bereikbaar.setter
    def bereikbaar(self, value):
        self._bereikbaar = set_boolean(value)

    @property
    def batterijpercentage(self):
        return self._batterijpercentage

    @batterijpercentage.setter
    def batterijpercentage(self, value):
        try:
            if 0 <= int(value) <= 100:
                self._batterijpercentage = int(value)
            else:
                raise SensorException("Batterijpercentage geen percentage: " + str(value))
        except ValueError:
            raise SensorException("Batterijpercentage geen integer: " + str(value))

    @property
    def tijdstip_meting(self):
        return self._tijdstip_meting

    @tijdstip_meting.setter
    def tijdstip_meting(self, value):
        self._tijdstip_meting = set_datetime(value)


class Schakelaar(Sensor):
    AAN = '1'
    DIMMER_OMHOOG = '2'
    DIMMER_OMLAAG = '3'
    UIT = '4'

    def __init__(self, volgnr):
        super(Schakelaar, self).__init__(volgnr)
        self._knop_id = -1
        self._knop_event = -1

    @property
    def knop_id(self):
        return self._knop_id

    @property
    def knop_event(self):
        return self._knop_event

    @knop_id.setter
    def knop_id(self, value):
        self._knop_event = value
        value = str(value)[0]
        if value in [Schakelaar.AAN, Schakelaar.DIMMER_OMHOOG, Schakelaar.DIMMER_OMLAAG, Schakelaar.UIT]:
            self._knop_id = value
        else:
            raise SensorException("Verkeerde knop waarde: " + str(value))

    @property
    def knop_waarde(self):
        if self._knop_id == Schakelaar.AAN:
            return 'aan'
        elif self._knop_id == Schakelaar.DIMMER_OMHOOG:
            return 'dimmer_omhoog'
        elif self._knop_id == Schakelaar.DIMMER_OMLAAG:
            return 'dimmer_omlaag'
        elif self._knop_id == Schakelaar.UIT:
            return 'uit'


class BewegingSchakelaar(Sensor):
    def __init__(self, volgnr):
        super(BewegingSchakelaar, self).__init__(volgnr)
        self._beweging_gesignaleerd = False

    @property
    def beweging_gesignaleerd(self):
        return self._beweging_gesignaleerd

    @beweging_gesignaleerd.setter
    def beweging_gesignaleerd(self, value):
        self._beweging_gesignaleerd = set_boolean(value)


class TemperatuurSensor(Sensor):
    def __init__(self, volgnr):
        super(TemperatuurSensor, self).__init__(volgnr)
        self._temperature = -1

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        try:
            self._temperature = int(value)
        except ValueError:
            raise SensorException("temperature geen integer: " + str(value))

    @property
    def temperature_celsius(self):
        return self._temperature / 100


class LichtSensor(Sensor):
    def __init__(self, volgnr):
        super(LichtSensor, self).__init__(volgnr)
        self._lichtniveau = -1

    @property
    def lichtniveau(self):
        return self._lichtniveau

    @lichtniveau.setter
    def lichtniveau(self, value):
        try:
            if int(value) >= 0:
                self._lichtniveau = int(value)
            else:
                raise SensorException("Lichtniveau te laag: " + str(value))
        except ValueError:
            raise SensorException("Lichtniveau geen integer")

    @property
    def lichtniveau_lux(self):
        if self._lichtniveau == 0:
            return 0
        return math.log10(self._lichtniveau)

    @property
    def lichtwaarde(self):
        if self._lichtniveau < 3000:
            return "Nacht licht"
        elif self._lichtniveau < 10000:
            return "Gedimmed licht"
        elif self._lichtniveau < 17000:
            return "Gezellig licht"
        elif self._lichtniveau < 22000:
            return "Normaal licht"
        elif self._lichtniveau < 25500:
            return "Werk of lees licht"
        elif self._lichtniveau < 28500:
            return "Gespecialiseerd fel licht"
        else:
            return "Maximum licht"


def set_boolean(value):
    if str(value).lower() == 'true':
        return True
    elif str(value).lower() == 'false':
        return False
    else:
        raise SensorException("Geen boolean: " + str(value))


def set_datetime(value):
    try:
        return datetime.datetime.fromisoformat(value)
    except ValueError:
        raise SensorException("Tijdstip ingedrukt geen isoformaat: " + str(value))
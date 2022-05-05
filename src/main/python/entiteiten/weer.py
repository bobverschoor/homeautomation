import inspect


# https://api.waqi.info/api/feed/@5387/aqi.json

def set_float(value, value_type, min, max):
    error = ""
    try:
        float_value = float(value)
        if float_value > max:
            error = value_type + " boven de ingestelde parameters (" + str(max) + ")" + \
                    str(float_value)
        if float_value < min:
            error = value_type + " beneden de ingestelde parameters: (" + str(min) + ")" + \
                    str(float_value)
    except ValueError:
        error = " waarde ongeldig: " + str(value)
        float_value = -1.0
    return float_value, error


class Weer:
    TEMP_MAX = 50.0
    TEMP_MIN = -50.0
    WIND_MIN = 0.0
    WIND_MAX = 50.0
    LUCHTDRUK_MIN = 850.0
    LUCHTDRUK_MAX = 1100.0
    NEERSLAG_MIN = 0.0
    NEERSLAG_MAX = 100.0
    NEERSLAG_INTENSITEIT_MIN = 0.0
    NEERSLAG_INTENSITEIT_MAX = 99999.0
    PERCENTAGE_MIN = 0
    PERCENTAGE_MAX = 100

    def __init__(self):
        self._locatie = {}
        self._temperatuur = 9999.99
        self._gevoelstemperatuur = 9999.99
        self._luchtvochtigheid = -1
        self._windrichting = -1.0
        self._windsnelheidms = 9999.99
        self._luchtdruk = 9999.99
        self._neerslaghoeveelheid24h = -1.0
        self._neerslagintensiteit = -1.0
        self._error = ""

    @property
    def temperatuur(self):
        return self._temperatuur

    @temperatuur.setter
    def temperatuur(self, value):
        self._temperatuur, self.error = set_float(value, "temperatuur", Weer.TEMP_MIN, Weer.TEMP_MAX)

    @property
    def gevoelstemperatuur(self):
        return self._gevoelstemperatuur

    @gevoelstemperatuur.setter
    def gevoelstemperatuur(self, value):
        self._gevoelstemperatuur, self.error = set_float(value, "gevoelstemperatuur", Weer.TEMP_MIN, Weer.TEMP_MAX)

    @property
    def windsnelheidms(self):
        return self._windsnelheidms

    @windsnelheidms.setter
    def windsnelheidms(self, value):
        self._windsnelheidms, self.error = set_float(value, "windsnelheidms", Weer.WIND_MIN, Weer.WIND_MAX)

    @property
    def luchtvochtigheid(self):
        return self._luchtvochtigheid

    @luchtvochtigheid.setter
    def luchtvochtigheid(self, value):
        self._luchtvochtigheid, self.error = set_float(value, "luchtvochtigheid",
                                                       Weer.PERCENTAGE_MIN, Weer.PERCENTAGE_MAX)
        self._luchtvochtigheid = int(self._luchtvochtigheid)

    @property
    def luchtdruk(self):
        return self._luchtdruk

    @luchtdruk.setter
    def luchtdruk(self, value):
        self._luchtdruk, self.error = set_float(value, "luchtdruk", Weer.LUCHTDRUK_MIN, Weer.LUCHTDRUK_MAX)

    @property
    def windrichting(self):
        return self._windrichting

    @windrichting.setter
    def windrichting(self, value):
        richting = ["Noord", "NNO", "NO", "ONO", "Oost", "OZO", "ZO", "ZZO", "Zuid",
                    "ZZW", "ZW", "WZW", "West", "WNW", "NW", "NNW"]
        graden = 0.0
        for r in richting:
            if value.lower() == r.lower():
                self._windrichting = graden
                break
            graden += 22.5
        if graden >= 360:
            self.error = "Onbekende windrichting: " + str(value)

    @property
    def neerslaghoeveelheid24h(self):
        return self._neerslaghoeveelheid24h

    @neerslaghoeveelheid24h.setter
    def neerslaghoeveelheid24h(self, value):
        self._neerslaghoeveelheid24h, self.error = set_float(value, "neerslaghoeveelheid",
                                                             Weer.NEERSLAG_MIN, Weer.NEERSLAG_MAX)

    @property
    def neerslagintensiteit(self):
        return self._neerslagintensiteit

    @neerslagintensiteit.setter
    def neerslagintensiteit(self, value):
        self._neerslagintensiteit, self.error = set_float(value, "neerslagintensiteit",
                                                          Weer.NEERSLAG_INTENSITEIT_MIN, Weer.NEERSLAG_INTENSITEIT_MAX)

    def set_locatie_for_meting(self, metingtype, locatie):
        self._locatie[metingtype] = locatie

    def get_locatie_of_meting(self, metingtype):
        return self._locatie[metingtype]

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        if value:
            self._error = self._error + "\n" + str(value)

    def get_properties(self):
        props = []
        for prop in self.__dir__():
            if not prop.startswith('_'):
                if not inspect.ismethod(getattr(self, prop)):
                    props.append((prop, self.__getattribute__(prop)))
        return props

import inspect


# https://api.waqi.info/api/feed/@5387/aqi.json

class Weer:

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
        try:
            self._temperatuur = float(value)
            if -50 > self._temperatuur > 50:
                self._error = "Temperatuur buiten de ingestelde parameters: " + str(self._temperatuur)
        except ValueError:
            self._error = "Temperatuur waarde ingeldig: " + str(value)

    @property
    def gevoelstemperatuur(self):
        return self._gevoelstemperatuur

    @gevoelstemperatuur.setter
    def gevoelstemperatuur(self, value):
        try:
            self._gevoelstemperatuur = float(value)
            if -50 > self._gevoelstemperatuur > 50:
                self._error = "GevoelsTemperatuur buiten de ingestelde parameters: " + str(self._gevoelstemperatuur)
        except ValueError:
            self._error = "gevoelsTemperatuur waarde ingeldig: " + str(value)

    @property
    def windsnelheidms(self):
        return self._windsnelheidms

    @windsnelheidms.setter
    def windsnelheidms(self, value):
        try:
            self._windsnelheidms = float(value)
            if 0 > self._windsnelheidms > 50:
                self._error = "windsnelheidms waarde ongeldig: " + str(value)
        except ValueError:
            self._error = "windsnelheidms waarde ongeldig: " + str(value)

    @property
    def luchtvochtigheid(self):
        return self._luchtvochtigheid

    @luchtvochtigheid.setter
    def luchtvochtigheid(self, value):
        try:
            self._luchtvochtigheid = int(value)
        except ValueError:
            self._error = "luchtvochtigheid waarde ingeldig: " + str(value)

    @property
    def luchtdruk(self):
        return self._luchtdruk

    @luchtdruk.setter
    def luchtdruk(self, value):
        try:
            self._luchtdruk = float(value)
            if 850 > self._luchtdruk > 1100:
                self._error = "Luchtdruk waarde te groot of te klein: " + str(self._luchtdruk)
        except ValueError:
            self._error = "luchtdruk waarde ingeldig: " + str(value)

    @property
    def windrichting(self):
        return self._windrichting

    @windrichting.setter
    def windrichting(self, value):
        if value == "Noord":
            value = 0
        elif value == "NNO":
            value = 22.5
        elif value == "NO":
            value = 45
        elif value == "ONO":
            value = 67.5
        elif value == "Oost":
            value = 90
        elif value == "OZO":
            value = 112.5
        elif value == "ZO":
            value = 135
        elif value == "ZZO":
            value = 157.5
        elif value == "Zuid":
            value = 180
        elif value == "ZZW":
            value = 202.5
        elif value == "ZW":
            value = 225
        elif value == "WZW":
            value = 247.5
        elif value == "West":
            value = 270
        elif value == "WNW":
            value = 292.5
        elif value == "NW":
            value = 315
        elif value == "NNW":
            value = 337.5
        else:
            self.error = "Onbekende windrichting: " + str(value)
        self._windrichting = float(value)

    @property
    def neerslaghoeveelheid24h(self):
        return self._neerslaghoeveelheid24h

    @neerslaghoeveelheid24h.setter
    def neerslaghoeveelheid24h(self, value):
        try:
            self._neerslaghoeveelheid24h = float(value)
            if self._neerslaghoeveelheid24h < 0:
                self._error = "neerslaghoeveelheid moet groter dan 0 zijn: " + str(self._neerslaghoeveelheid24h)
        except ValueError:
            self._error = "neerslaghoeveelheid waarde ingeldig: " + str(value)

    @property
    def neerslagintensiteit(self):
        return self._neerslagintensiteit

    @neerslagintensiteit.setter
    def neerslagintensiteit(self, value):
        try:
            self._neerslagintensiteit = float(value)
            if self._neerslagintensiteit < 0:
                self._error = "neerslagintensiteit moet groter dan 0 zijn: " + str(self._neerslagintensiteit)
        except ValueError:
            self._error = "neerslagintensiteit waarde ingeldig: " + str(value)

    def set_locatie_for_meting(self, metingtype, locatie):
        self._locatie[metingtype] = locatie

    def get_locatie_of_meting(self, metingtype):
        return self._locatie[metingtype]

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = self._error + "\n" + value

    def get_properties(self):
        props = []
        for prop in self.__dir__():
            if not prop.startswith('_'):
                if not inspect.ismethod(getattr(self, prop)):
                    props.append((prop, self.__getattribute__(prop)))
        return props

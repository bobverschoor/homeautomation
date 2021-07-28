class Weer:
    def __init__(self):
        self._locatie = ""
        self._temperatuur = 9999.99
        self._gevoelstemperatuur = 9999.99
        self._luchtvochtigheid = -1
        self._windrichting = ""
        self._windsnelheidms = 9999.99
        self._luchtdruk = 9999.99
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
    def locatie(self):
        return self._locatie

    @locatie.setter
    def locatie(self, value):
        self._locatie = value

    @property
    def windrichting(self):
        return self._windrichting

    @windrichting.setter
    def windrichting(self, value):
        if value in ["Noord", "NNO", "NO", "ONO", "Oost", "OZO", "ZO",
                     "ZZO", "Zuid", "ZZW", "ZW", "WZW", "West", "WNW", "NW", "NWN"]:
            self._windrichting = value
        else:
            print("Onbekende windrichting: " + value)

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = self._error + "\n" + value

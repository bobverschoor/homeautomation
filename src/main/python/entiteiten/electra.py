import datetime


class Electra:
    LAAGTARIEF = "laag"
    HOOGTARIEF = "hoog"
    CONSUMENT = "consument"
    PRODUCENT = "producent"

    def __init__(self):
        self._tarief = ""
        self._richting = ""
        self._wh = -1
        self._timestamp = datetime.datetime.now(datetime.timezone.utc)

    @property
    def tarief(self):
        return self._tarief

    @tarief.setter
    def tarief(self, value):
        if value in [Electra.LAAGTARIEF, Electra.HOOGTARIEF]:
            self._tarief = value
        else:
            raise ValueError("Wrong tarief: " + str(value))

    @property
    def richting(self):
        return self._richting

    @richting.setter
    def richting(self, value):
        if value in [Electra.CONSUMENT, Electra.PRODUCENT]:
            self._richting = value
        else:
            raise ValueError("Wrong direction: " + str(value))

    @property
    def wh(self):
        return self._wh

    @wh.setter
    def wh(self, value):
        if value >= 0:
            self._wh = value
        else:
            raise ValueError("invalid wh: " + str(value))

    @property
    def timestamp(self):
        return self._timestamp

    def __str__(self):
        return "tarief: " + self._tarief + ", richting: " + self._richting + ", Wh: " + str(self._wh) + \
                ", time: " + str(self._timestamp)
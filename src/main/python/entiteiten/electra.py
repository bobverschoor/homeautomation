
from entiteiten.meetwaarde import Meetwaarde


class Electra(Meetwaarde):
    LAAGTARIEF = "laag"
    HOOGTARIEF = "hoog"
    VERBRUIKT = "verbruikt"
    GELEVERD = "geleverd"

    def __init__(self):
        super().__init__("Wh")
        self._tarief = ""
        self._richting = ""

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
        if value in [Electra.VERBRUIKT, Electra.GELEVERD]:
            self._richting = value
        else:
            raise ValueError("Wrong direction: " + str(value))

    def __str__(self):
        return "tarief: " + self._tarief + ", richting: " + self._richting + ", Wh: " + str(self._waarde) + \
                ", tijdstip: " + str(self._timestamp)

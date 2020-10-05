
from entiteiten.meetwaarde import Meetwaarde


class Gas(Meetwaarde):
    def __init__(self):
        super().__init__("m3")

    def __str__(self):
        return "m3: " + str(self._waarde) + ", tijdstip: " + str(self._timestamp)
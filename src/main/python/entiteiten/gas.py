from dataclasses import dataclass

from entiteiten.meetwaarde import Meetwaarde


@dataclass(frozen=True, init=True)
class Gas(Meetwaarde):

    eenheid: str = "m3"

    def __repr__(self):
        return "m3: " + str(self.waarde) + ", tijdstip: " + str(self.timestamp)
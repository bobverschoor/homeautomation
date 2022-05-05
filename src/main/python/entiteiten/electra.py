from dataclasses import dataclass

from entiteiten.meetwaarde import Meetwaarde


@dataclass(frozen=True, init=True)
class Electra(Meetwaarde):
    LAAGTARIEF = "laag"
    HOOGTARIEF = "hoog"
    VERBRUIKT = "verbruikt"
    GELEVERD = "geleverd"
    FASE = "fase"

    eenheid: str = "Wh"
    tarief: str = ""
    richting: str = ""
    fase: str = ""

    def __post_init__(self):
        if self.tarief in [Electra.LAAGTARIEF, Electra.HOOGTARIEF]:
            self.tags["tarief"] = str(self.tarief)
        else:
            raise ValueError("Wrong tarief: " + str(self.tarief))
        if self.richting in [Electra.VERBRUIKT, Electra.GELEVERD]:
            self.tags["richting"] = str(self.richting)
        else:
            raise ValueError("Wrong direction: " + str(self.richting))

    def __repr__(self):
        return str(super().__repr__()) + ", tarief: " + self.tarief + ", richting: " + self.richting + \
               ", fase: " + self.fase

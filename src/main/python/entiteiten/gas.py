from dataclasses import dataclass

from entiteiten.meetwaarde import Meetwaarde


@dataclass(frozen=True, init=True)
class Gas(Meetwaarde):

    eenheid: str = "m3"

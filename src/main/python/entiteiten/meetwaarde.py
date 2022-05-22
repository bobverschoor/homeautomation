import datetime
from dataclasses import dataclass


def convertstr2tags(value: str):
    return convertlist2tags([value])


def convertlist2tags(values: list):
    dictionairy = {}
    for item in values:
        if ":" in item:
            naam, waarde = item.split(":")
            dictionairy[naam.strip()] = waarde.strip()
        else:
            raise ValueError("invalid value: " + str(values))
    return dictionairy


@dataclass(frozen=True, init=True)
class Meetwaarde:
    waarde: float
    tags: dict
    eenheid: str
    timestamp: datetime = datetime.datetime.now(datetime.timezone.utc)

    def __repr__(self):
        if self.tags == {}:
            tstr = ""
        else:
            tstr = ", tags:"
            for t in self.tags.keys():
                tstr = tstr + " " + str(t) + "=" + str(self.tags[t])
        return str(self.waarde) + " " + self.eenheid + tstr

    def __str__(self):
        return self.__repr__()

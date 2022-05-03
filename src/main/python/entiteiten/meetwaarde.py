import datetime
from dataclasses import dataclass


def convert2tags(value):
    dictionairy = {}
    if isinstance(value, str):
        values = [value]
    else:
        values = value
    for item in values:
        if ":" in item:
            naam, waarde = item.split(":")
            dictionairy[naam] = waarde.strip()
        else:
            raise ValueError("invalid value: " + str(value))
    return dictionairy


def convert2timestamp(value):
    if isinstance(value, datetime.datetime):
        timestamp = value
    elif value >= 0:
        try:
            timestamp = datetime.datetime.fromtimestamp(value)
        except Exception as e:
            raise ValueError(e)
    else:
        raise ValueError("value no timestamp: " + str(value))
    return timestamp


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

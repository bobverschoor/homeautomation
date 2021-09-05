import datetime
import re

from entiteiten.meetwaarde import Meetwaarde


class WoningGateway:

    def __init__(self):
        self.bridge = None

    def get_meetwaarden(self):
        meetwaarden = []
        if self.bridge is None:
            raise ModuleNotFoundError("Bridge device not set")
        for licht in self.bridge.get_alle_lichten():
            meetwaarde = Meetwaarde('licht_aan')
            meetwaarde.timestamp = datetime.datetime.now()
            meetwaarde.waarde = licht.aan
            meetwaarde.tags = "naam:" + licht.naam
            meetwaarde.tags = "id:" + non_alphanumeric_chars(licht.unique_id)
            meetwaarden.append(meetwaarde)
        return meetwaarden


def non_alphanumeric_chars(input):
    output = re.sub(r'\W+', '', input)
    return output
import datetime


class Meetwaarde:
    def __init__(self, eenheid):
        self._waarde = ""
        self._eenheid = eenheid
        self._tags = {}
        self._timestamp = datetime.datetime.now(datetime.timezone.utc)
        self._slimmemeter = None

    @property
    def eenheid(self):
        return self._eenheid

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        if ":" in value:
            tagnaam, tagvalue = value.split(":")
            self._tags[tagnaam] = tagvalue
        else:
            raise ValueError("invalid tag: " + str(value))

    @property
    def waarde(self):
        return self._waarde

    @waarde.setter
    def waarde(self, value):
        if value >= 0:
            self._waarde = value
        else:
            raise ValueError("invalid value: " + str(value))

    @property
    def timestamp(self):
        return int(self._timestamp.timestamp())

    @timestamp.setter
    def timestamp(self, value):
        if isinstance(value, datetime.datetime):
            self._timestamp = value
        elif value >= 0:
            try:
                self._timestamp = datetime.datetime.fromtimestamp(value)
            except Exception as e:
                raise ValueError(e)
        else:
            raise ValueError("m3 value below zero: " + str(value))

    @property
    def slimmemeter(self):
        return self._slimmemeter

    @slimmemeter.setter
    def slimmemeter(self, sm):
        self._slimmemeter = sm
        self.tags = "meternaam:" + sm.naam
        self.tags = "metertype:" + sm.type

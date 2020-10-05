import datetime

class Meetwaarde:
    def __init__(self, eenheid):
        self._waarde = ""
        self.eenheid = eenheid
        self._timestamp = datetime.datetime.now(datetime.timezone.utc)

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
        return self._timestamp

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

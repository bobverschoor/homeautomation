import datetime

class Gas:
    def __init__(self):
        self._m3 = -1
        self._timestamp = datetime.datetime.now(datetime.timezone.utc)

    @property
    def m3(self):
        return self._m3

    @m3.setter
    def m3(self, value):
        if value >= 0:
            self._m3 = value
        else:
            raise ValueError("m3 value below zero: " + str(value))

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


    def __str__(self):
        return "m3: " + str(self._m3) + ", tijdstip: " + str(self._timestamp)
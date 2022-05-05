class LichtException(Exception):
    def __init__(self, message):
        super(LichtException, self).__init__(message)


class Licht:
    def __init__(self, volgnr):
        try:
            self._volgnr = int(volgnr)
        except ValueError as ve:
            raise LichtException(ve)
        self._unique_id = ""
        self._aan = None
        self._bereikbaar = None
        self._naam = ""

    @property
    def volgnr(self):
        return self._volgnr

    @property
    def naam(self):
        return self._naam

    @naam.setter
    def naam(self, value):
        self._naam = value

    @property
    def aan(self):
        return self._aan

    @property
    def unique_id(self):
        return self._unique_id

    @unique_id.setter
    def unique_id(self, value):
        self._unique_id = value

    @aan.setter
    def aan(self, value):
        self._aan = set_boolean(value)

    @property
    def bereikbaar(self):
        if self._bereikbaar is None:
            return False
        return self._bereikbaar

    @bereikbaar.setter
    def bereikbaar(self, value):
        self._bereikbaar = set_boolean(value)


def set_boolean(value):
    if str(value).lower() in ["true", "1"]:
        return True
    elif str(value).lower() in ["false", "0"]:
        return False
    else:
        raise LichtException("Geen boolean: " + str(value))

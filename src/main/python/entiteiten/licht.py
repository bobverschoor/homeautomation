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
        if is_boolean(value):
            self._aan = value
        else:
            raise LichtException("Incorrect value voor aan: " + str(value))

    @property
    def bereikbaar(self):
        return self._bereikbaar

    @bereikbaar.setter
    def bereikbaar(self, value):
        if str(value) in ['True', 'False']:
            self._bereikbaar = value
        else:
            raise LichtException("Incorrect value voor bereikbaarheid: " + str(value))

    def __str__(self):
        return self._unique_id + " " + self._naam + " : " + str(self._aan)


def is_boolean(value):
    if str(value) in ['True', 'False']:
        return True
    return False

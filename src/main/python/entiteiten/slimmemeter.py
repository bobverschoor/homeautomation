class Slimmemeter():
    def __init__(self, header):
        self._naam, self._type = header.split('\\')

    @property
    def naam(self):
        return self._naam

    @property
    def type(self):
        return self._type

class Slimmemeter():
    def __init__(self, header):
        header = header.strip()
        header = header.strip('//')
        self._naam, self._type = header.split('\\')


    @property
    def naam(self):
        return self._naam

    @property
    def type(self):
        return self._type

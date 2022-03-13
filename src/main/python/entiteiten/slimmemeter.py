class Slimmemeter:
    def __init__(self, header):
        header = header.strip()
        header = header.strip('//')
        if header == "":
            print("Header is empty")
        else:
            try:
                self._naam, self._type = header.split('\\')
            except ValueError:
                print("header of wrong format:" + str(header))

    @property
    def naam(self):
        return self._naam

    @property
    def type(self):
        return self._type

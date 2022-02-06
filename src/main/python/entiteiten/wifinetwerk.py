class WifiNetwerk:
    def __init__(self):
        self._channel = -1
        self._frequency_ghz = -1
        self._quality_percentage = -1
        self._signallevel_dbm = -1
        self._essid = ""

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        self._channel = int(value)

    @property
    def essid(self):
        return self._essid

    @essid.setter
    def essid(self, value):
        self._essid = value

    @property
    def frequency_ghz(self):
        return self._frequency_ghz

    @frequency_ghz.setter
    def frequency_ghz(self, value):
        self._frequency_ghz = float(value)

    @property
    def quality_percentage(self):
        return self._quality_percentage

    @quality_percentage.setter
    def quality_percentage(self, value):
        t, n = value.split('/')
        self._quality_percentage = int(t) / int(n)

    @property
    def signallevel_dbm(self):
        return self._signallevel_dbm

    @signallevel_dbm.setter
    def signallevel_dbm(self, value):
        self._signallevel_dbm = float(value)

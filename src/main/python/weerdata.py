import configparser
from persistence.database_gateway import DatabaseGateway
from sensor.weerlive_api import WeerLive


class WeerGateway:
    def __init__(self):
        self.weer_device = None

    def get_meetwaarden(self):
        if self.weer_device is None:
            raise ModuleNotFoundError("weer device not set")
        weerdata = self.weer_device.get_weerdata()


class WeerdataController:
    def __init__(self, configfile):
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._weerdata = WeerGateway()
        self._weerdata.weer_device = WeerLive(self._config)
        self._databasebase = DatabaseGateway()

    def collect_store(self):
        meetwaarden = self._weerdata.get_meetwaarden()
        print(meetwaarden)
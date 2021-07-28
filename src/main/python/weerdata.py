import configparser
import datetime
import os

from persistence.database_gateway import DatabaseGateway
from sensor.weer_gateway import WeerGateway
from sensor.weerlive_api import WeerLiveDevice


class WeerdataController:
    def __init__(self, configfile):
        self._config = configparser.ConfigParser()
        if os.path.exists(configfile):
            self._config.read(configfile)
            self._weerdata = WeerGateway()
            self._weerdata.weer_device = WeerLiveDevice(self._config)
            self._databasebase = DatabaseGateway("weer")
        else:
            print("Config file does not exist: " + str(configfile) + ", cwd: " + os.getcwd())
            exit(1)

    def collect_store(self):
        meetwaarden = self._weerdata.get_meetwaarden()
        for meetwaarde in meetwaarden:
            self._databasebase.entiteiten = meetwaarde
            self._databasebase.store()


if __name__ == "__main__":
    print(datetime.datetime.now())
    WeerdataController('src/main/resources/secrets.ini').collect_store()
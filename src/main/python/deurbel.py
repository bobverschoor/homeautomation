import configparser
import os

from sensor.deurbel_gateway import DeurbelGateway


class DeurbelController:

    def __init__(self, configfile, dryrun=False):
        self._store_in_database = not dryrun
        self._config = configparser.ConfigParser()
        if os.path.exists(configfile):
            self._config.read(configfile)
            self._deurbel = DeurbelGateway()
            self._deurbel.set_deurbel(self._config)
            # if self._store_in_database:
            #     self._databasebase = DatabaseGateway(self._config['p1meter']['databasenaam'])
            # else:
            #     self._databasebase = DatabaseGateway("dryrun")
        else:
            print("Config file does not exist: " + str(configfile) + ", cwd: " + os.getcwd())
            exit(1)


import argparse
import configparser
import datetime
import os
from pid import PidFile

from sensor.deurbel_gateway import DeurbelGateway


class DeurbelController:

    def __init__(self, configfile, dryrun=False):
        self._store_in_database = not dryrun
        self._config = configparser.ConfigParser()
        if os.path.exists(configfile):
            self._config.read(configfile)
            self._deurbel = DeurbelGateway(self._config)
            # if self._store_in_database:
            #     self._databasebase = DatabaseGateway(self._config['p1meter']['databasenaam'])
            # else:
            #     self._databasebase = DatabaseGateway("dryrun")
        else:
            print("Config file does not exist: " + str(configfile) + ", cwd: " + os.getcwd())
            exit(1)

    def control_loop(self):
        while True:
            try:
                if self._deurbel.someone_at_the_deur():
                    print("stuur een berichtje")
            except Exception as e:
                print(e)


if __name__ == "__main__":
    with PidFile():
        parser = argparse.ArgumentParser(description='Start the waiting for deurbel.')
        args = parser.parse_args()
        print(datetime.datetime.now())
        DeurbelController('src/main/resources/secrets.ini', dryrun=args.dryrun).control_loop()

import argparse
import configparser
import datetime
import os

from gateways.internet_gateway import InternetGateway
from persistence.database_gateway import DatabaseGateway
from persistence.influxdb_device import InFluxDBDevice


class InternetController:
    CONFIG_DATABASENAAM = 'databasenaam'

    def __init__(self, configfile, dryrun=False):
        self._store_in_database = not dryrun
        self._config = configparser.ConfigParser()
        if os.path.exists(configfile):
            self._config.read(configfile)
            self._internet = InternetGateway(self._config['internet'])
            self._internet.load_devices()
            if self._store_in_database:
                self._databasebase = DatabaseGateway(InFluxDBDevice(self._config['internet']['databasenaam']))
            else:
                self._databasebase = DatabaseGateway("dryrun")
        else:
            print("Config file does not exist: " + str(configfile) + ", cwd: " + os.getcwd())
            exit(1)

    def collect_store(self):
        internetmeetwaarden = self._internet.get_meetwaarden()
        for meetwaarde in internetmeetwaarden:
            self._databasebase.entiteiten = meetwaarde
        if self._store_in_database:
            self._databasebase.store()
        else:
            print(str(self._databasebase))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Collect internet (speed) data and stores it in a database.')
    parser.add_argument('--dryrun', help='collect data but do not store in database.', action="store_true")
    args = parser.parse_args()
    if args.dryrun:
        print("dryrun mode")
    print(datetime.datetime.now())
    controller = InternetController('src/main/resources/secrets.ini', dryrun=args.dryrun)
    controller.collect_store()

import argparse
import configparser
import datetime
import os

from persistence.database_gateway import DatabaseGateway
from device.sensor.dsmr_50_device import DSMR_50
from gateways.slimmemeter_gateway import SlimmemeterGateway


class EnergieMeterController:
    def __init__(self, configfile, dryrun=False):
        self._store_in_database = not dryrun
        self._config = configparser.ConfigParser()
        if os.path.exists(configfile):
            self._config.read(configfile)
            self._slimmemeter = SlimmemeterGateway()
            self._slimmemeter.p1 = DSMR_50(self._config)
            if self._store_in_database:
                self._databasebase = DatabaseGateway(self._config['p1meter']['databasenaam'])
            else:
                self._databasebase = DatabaseGateway("dryrun")
        else:
            print("Config file does not exist: " + str(configfile) + ", cwd: " + os.getcwd())
            exit(1)

    def collect_store(self):
        meetwaarden = self._slimmemeter.get_meetwaarden()
        for meetwaarde in meetwaarden:
            self._databasebase.entiteiten = meetwaarde
        if self._store_in_database:
            self._databasebase.store()
        else:
            self._databasebase.print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Collect p1 smartmeter data and stores it in a database.')
    parser.add_argument('--dryrun', help='collect data but do not store in database.', action="store_true")
    args = parser.parse_args()
    if args.dryrun:
        print("dryrun mode" )
    print(datetime.datetime.now())
    EnergieMeterController('src/main/resources/secrets.ini', dryrun=args.dryrun).collect_store()
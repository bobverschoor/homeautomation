import argparse
import configparser
import datetime
import os
import time

from device.arp import Arp
from device.hue_bridge_device import HueBridgeDevice
from entiteiten.user import User
from gateways.network_gateway import NetworkGateway
from gateways.woning_gateway import WoningGateway
from persistence.database_gateway import DatabaseGateway


class WoningController:
    CONFIG_PRE_USER = 'user_'

    def __init__(self, configfile, dryrun=False):
        self._store_in_database = not dryrun
        self._config = configparser.ConfigParser()
        if os.path.exists(configfile):
            self._config.read(configfile)
            self._woning = WoningGateway()
            self._woning.bridge = HueBridgeDevice(self._config)
            self._users = self.get_users_from_config()
            self._network = NetworkGateway(self._config, self._users)
            self._network.set_network_device(Arp(self._config))
            if self._store_in_database:
                self._databasebase = DatabaseGateway(self._config[HueBridgeDevice.CONFIG_HUEBRIDGE]['databasenaam'])
            else:
                self._databasebase = DatabaseGateway("dryrun")
        else:
            print("Config file does not exist: " + str(configfile) + ", cwd: " + os.getcwd())
            exit(1)

    def collect_store(self):
        woningmeetwaarden = self._woning.get_meetwaarden()
        for meetwaarde in woningmeetwaarden:
            self._databasebase.entiteiten = meetwaarde
        networkmeetwaarden = self._network.get_meetwaarden()
        for meetwaarde in networkmeetwaarden:
            self._databasebase.entiteiten = meetwaarde
        if self._store_in_database:
            self._databasebase.store()
        else:
            self._databasebase.print()

    def alarmeer_groep(self):
        self._woning.alarmeer_lichten_in_groep()

    def get_users_from_config(self):
        users = []
        for user_id in range(1,10):
            usersection = WoningController.CONFIG_PRE_USER + str(user_id)
            if self._config.has_section(usersection):
                users.append(User(self._config[usersection]))
        return users


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Collect woning data and stores it in a database.')
    parser.add_argument('--dryrun', help='collect data but do not store in database.', action="store_true")
    parser.add_argument('--testalerting', help='Test the alerting of lights', action="store_true")
    args = parser.parse_args()
    if args.dryrun:
        print("dryrun mode" )
    print(datetime.datetime.now())
    controller = WoningController('src/main/resources/secrets.ini', dryrun=args.dryrun)
    controller.collect_store()
    if args.testalerting:
        print("test alerting of lights")
        controller.alarmeer_groep()
        time.sleep(5)
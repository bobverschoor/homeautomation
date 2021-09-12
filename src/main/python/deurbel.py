import argparse
import configparser
import datetime
import os
import time

from pid import PidFile, PidFileAlreadyLockedError

from device.hue_bridge_device import HueBridgeDevice, HueBridgeException
from device.telegram_device import TelegramDevice
from gateways.deurbel_gateway import DeurbelGateway
from gateways.messenger_gateway import MessengerGateway
from gateways.woning_gateway import WoningGateway
from persistence.database_gateway import DatabaseGateway


class DeurbelController:

    def __init__(self, configfile, debug=False):
        config = configparser.ConfigParser()
        self._debug = debug
        if os.path.exists(configfile):
            config.read(configfile)
            self._deurbel = DeurbelGateway(config,  debug=debug)
            self._messenger = MessengerGateway(config, debug=debug)
            self._messenger.setup(TelegramDevice(config))
            if DeurbelGateway.CONFIG_DATABASENAAM in config[DeurbelGateway.CONFIG_DEURBEL]:
                self._databasebase = DatabaseGateway(
                    config[DeurbelGateway.CONFIG_DEURBEL][DeurbelGateway.CONFIG_DATABASENAAM])
            else:
                print("Databasenaam not in config, therefore not storing results in database.")
                self._databasebase = None
            try:
                self._woning = WoningGateway()
                self._woning.bridge = HueBridgeDevice(config)
            except HueBridgeException as hbe:
                self._woning = None
                print(hbe)
                print("Skipping hue")
        else:
            print("Config file does not exist: " + str(configfile) + ", cwd: " + os.getcwd())
            exit(1)

    def answer_door(self):
        meetwaarde = self._deurbel.someone_at_the_deur()
        if meetwaarde.waarde:
            if self._debug:
                print(str(datetime.datetime.now()) + " Someone at the door")
            self._messenger.send_text_someone_at_the_door()
        return meetwaarde

    def control_loop(self, response_time=0.1):
        loopcount = 0
        # elke minuut loggen. 1 / response_time
        while response_time > 0:
            try:
                meetwaarde = self.answer_door()
                if self._woning:
                    self._woning.alarmeer_lichten_in_groep()
                elke_10_minuut_loggen = int((1 / response_time) * 600)
                if self._databasebase:
                    if meetwaarde.waarde:
                        self._databasebase.entiteiten = meetwaarde
                        self._databasebase.store()
                    elif loopcount > elke_10_minuut_loggen:
                        self._databasebase.entiteiten = meetwaarde
                        self._databasebase.store()
                        loopcount = 0
                time.sleep(response_time)
                loopcount += 1
            except Exception as exc:
                print(str(datetime.datetime.now()) + " " + str(exc))


if __name__ == "__main__":
    try:
        debug_arg = False
        with PidFile("/tmp/deurbel.py"):
            parser = argparse.ArgumentParser(description='Start the waiting for deurbel.')
            parser.add_argument('--debug', help='Log extra information.', action="store_true")
            args = parser.parse_args()
            if args.debug:
                debug_arg = True
            print(datetime.datetime.now())
            DeurbelController('src/main/resources/secrets.ini', debug=debug_arg).control_loop()
    except PidFileAlreadyLockedError:
        if debug_arg:
            print("Other proces still running (which is OK): " + str(datetime.datetime.now()))

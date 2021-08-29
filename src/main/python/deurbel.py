import argparse
import configparser
import datetime
import os
import time

from pid import PidFile, PidFileAlreadyLockedError

from device.telegram_device import TelegramDevice
from gateways.deurbel_gateway import DeurbelGateway
from gateways.messenger_gateway import MessengerGateway


class DeurbelController:

    def __init__(self, configfile, debug=False):
        self._config = configparser.ConfigParser()
        self._debug = debug
        if os.path.exists(configfile):
            self._config.read(configfile)
            self._deurbel = DeurbelGateway(self._config,  debug=debug)
            self._messenger = MessengerGateway(self._config, debug=debug)
            self._messenger.setup(TelegramDevice(self._config))
        else:
            print("Config file does not exist: " + str(configfile) + ", cwd: " + os.getcwd())
            exit(1)

    def answer_door(self):
        if self._deurbel.someone_at_the_deur():
            if self._debug:
                print(str(datetime.datetime.now()) + " Someone at the door")
            self._messenger.send_text_someone_at_the_door()

    def control_loop(self, response_time=0.1):
        while True:
            try:
                self.answer_door()
                time.sleep(response_time)
            except Exception as exc:
                print(str(datetime.datetime.now()) + " " + str(exc))


if __name__ == "__main__":
    try:
        with PidFile("/tmp/deurbel.py"):
            debug_arg = False
            parser = argparse.ArgumentParser(description='Start the waiting for deurbel.')
            parser.add_argument('--debug', help='Log extra information.', action="store_true")
            args = parser.parse_args()
            if args.debug:
                debug_arg = True
            print(datetime.datetime.now())
            DeurbelController('src/main/resources/secrets.ini', debug=debug_arg).control_loop()
    except PidFileAlreadyLockedError:
        print("Other proces still running (which is OK): " + str(datetime.datetime.now()))

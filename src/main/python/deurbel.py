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

    def __init__(self, configfile):
        self._config = configparser.ConfigParser()
        if os.path.exists(configfile):
            self._config.read(configfile)
            self._deurbel = DeurbelGateway(self._config)
            self._messenger = MessengerGateway()
            self._messenger.setup(TelegramDevice(self._config))
            self._testing = False
        else:
            print("Config file does not exist: " + str(configfile) + ", cwd: " + os.getcwd())
            exit(1)

    def control_loop(self):
        while True:
            try:
                if self._deurbel.someone_at_the_deur():
                    self._messenger.send("Er staat iemand voor de deur.")
                time.sleep(0.05)
                if self._testing:
                    break
            except Exception as e:
                print(str(datetime.datetime.now()) + " " + str(e))


if __name__ == "__main__":
    try:
        with PidFile("deurbel.py"):
            parser = argparse.ArgumentParser(description='Start the waiting for deurbel.')
            args = parser.parse_args()
            print(datetime.datetime.now())
            DeurbelController('src/main/resources/secrets.ini').control_loop()
    except PidFileAlreadyLockedError as e:
        print("Other proces still running (which is OK): " + str(datetime.datetime.now()))

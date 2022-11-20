import json
import os.path
import subprocess


class SpeedtestDeviceException(Exception):
    def __init__(self, message):
        super(SpeedtestDeviceException, self).__init__(message)


class SpeedtestDevice:
    SPEEDTEST_PATH = 'cli_path'

    def __init__(self, config):
        self._testdata = None
        self._config = config
        self._speedtest_path = None
        self.type = "speedtest"

    def loaded(self):
        if SpeedtestDevice.SPEEDTEST_PATH in self._config:
            self._speedtest_path = self._config[SpeedtestDevice.SPEEDTEST_PATH]
            if os.path.exists(self._speedtest_path):
                return True
        return False

    def get_download_speed(self):
        return float(self._get_from_subitem('download'))

    def get_upload_speed(self):
        return float(self._get_from_subitem('upload'))

    def get_ping_speed(self):
        return float(self._get_from_subitem('ping'))

    def get_server_name(self):
        return self._get_from_subitem('server', 'name')

    def get_server_distance(self):
        return int(self._get_from_subitem('server', 'd'))

    def get_client_ip(self):
        return self._get_from_subitem('client', 'ip')

    def _get_validated_data(self, max_distance=110, max_retries=10):
        invalid = True
        nr_of_times = 0
        data = None
        while invalid:
            nr_of_times += 1
            data = self._gettest_data()
            if "server" in data and "d" in data["server"]:
                afstand = int(data["server"]["d"])
                if afstand < max_distance:
                    invalid = False
            if nr_of_times > max_retries:
                invalid = False
            if invalid:
                self._testdata = None
        return data

    def _gettest_data(self):
        if self._testdata is None:
            try:
                self._testdata = json.loads(subprocess.check_output([self._speedtest_path, '--json', '--secure']))
            except subprocess.CalledProcessError:
                raise SpeedtestDeviceException("Speedtest failed.")
        return self._testdata

    def _get_from_subitem(self, name, sub=""):
        data = self._get_validated_data()
        if name in data:
            if sub:
                if sub in data[name]:
                    return data[name][sub]
            else:
                return data[name]
        else:
            raise SpeedtestDeviceException(name + " " + sub + " data not found: " + str(data))

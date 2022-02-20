
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
        data = self._gettest_data()
        if 'download' in data:
            return float(data['download'])
        else:
            raise SpeedtestDeviceException("Download data not found: " + str(data))

    def get_upload_speed(self):
        data = self._gettest_data()
        if 'upload' in data:
            return float(data['upload'])
        else:
            raise SpeedtestDeviceException("Upload data not found: " + str(data))

    def get_ping_speed(self):
        data = self._gettest_data()
        if 'ping' in data:
            return float(data['ping'])
        else:
            raise SpeedtestDeviceException("Ping data not found: " + str(data))

    def get_server_id(self):
        data = self._gettest_data()
        if 'server' in data and 'id' in data['server']:
            return int(data['server']['id'])
        else:
            raise SpeedtestDeviceException("Server Id data not found: " + str(data))

    def get_server_name(self):
        data = self._gettest_data()
        if 'server' in data and 'name' in data['server']:
            return data['server']['name']
        else:
            raise SpeedtestDeviceException("Server name data not found: " + str(data))

    def get_server_distance(self):
        data = self._gettest_data()
        if 'server' in data and 'd' in data['server']:
            return float(data['server']['d'])
        else:
            raise SpeedtestDeviceException("Server d data not found: " + str(data))

    def get_client_ip(self):
        data = self._gettest_data()
        if 'client' in data and 'ip' in data['client']:
            return data['client']['ip']
        else:
            raise SpeedtestDeviceException("Client IP data not found: " + str(data))

    def _gettest_data(self):
        if self._testdata is None:
            try:
                self._testdata = json.loads(subprocess.check_output([self._speedtest_path, '--json']))
            except subprocess.CalledProcessError:
                raise SpeedtestDeviceException("Speedtest failed.")
        return self._testdata



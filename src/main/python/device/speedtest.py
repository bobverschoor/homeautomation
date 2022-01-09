# {"download": 91706271.43394412, "upload": 27485708.776732102, "ping": 22.615,
#  "server": {"url": "http://speedtest.breedband.nl:8080/speedtest/upload.php", "lat": "51.9833", "lon": "5.9167",
#             "name": "Arnhem", "country": "Netherlands", "cc": "NL", "sponsor": "Breedband", "id": "5252",
#             "host": "speedtest.breedband.nl:8080", "d": 104.06065955630943, "latency": 22.615},
#  "timestamp": "2022-01-08T15:15:14.942401Z", "bytes_sent": 34512896, "bytes_received": 114977956, "share": null,
#  "client": {"ip": "217.123.109.107", "lat": "52.4594", "lon": "4.6015", "isp": "Ziggo", "isprating": "3.7",
#             "rating": "0", "ispdlavg": "0", "ispulavg": "0", "loggedin": "0", "country": "NL"}}
import json
import os.path
import subprocess


class SpeedtestDeviceException(Exception):
    def __init__(self, message):
        super(SpeedtestDeviceException, self).__init__(message)


class SpeedtestDevice:
    def __init__(self, config):
        self._testdata = None
        self._speedtest_path = config['cli_path']
        if not os.path.exists(self._speedtest_path):
            raise ModuleNotFoundError

    def get_download_speed(self):
        data = self._gettest_data()
        if 'download' in data:
            return data['download']
        else:
            raise SpeedtestDeviceException("Download data not found: " + str(data))

    def get_upload_speed(self):
        data = self._gettest_data()
        if 'upload' in data:
            return data['upload']
        else:
            raise SpeedtestDeviceException("Upload data not found: " + str(data))

    def get_ping_speed(self):
        data = self._gettest_data()
        if 'ping' in data:
            return data['ping']
        else:
            raise SpeedtestDeviceException("Ping data not found: " + str(data))

    def get_server_id(self):
        data = self._gettest_data()
        if 'server' in data and 'id' in data['server']:
            return data['server']['id']
        else:
            raise SpeedtestDeviceException("Server Id data not found: " + str(data))

    def get_client_ip(self):
        data = self._gettest_data()
        if 'client' in data and 'ip' in data['client']:
            return data['client']['ip']
        else:
            raise SpeedtestDeviceException("Client IP data not found: " + str(data))

    def _gettest_data(self):
        if self._testdata is None:
            self._testdata = json.loads(subprocess.check_output([self._speedtest_path, '--json']))
        return self._testdata



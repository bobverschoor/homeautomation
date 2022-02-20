import re
import subprocess

from entiteiten.wifinetwerk import WifiNetwerk


class WifiDeviceException(Exception):
    def __init__(self, message):
        super(WifiDeviceException, self).__init__(message)


class WifiDevice:
    CHANNEl = re.compile(r"\s+Channel:(\d+)")
    STARTNETWERK = re.compile("\s+Cell\s+\d+ - Address")
    ESSID = re.compile(r"\s+ESSID:\"(.+)\"")
    FREQUENCY = re.compile(r"\s+Frequency:(\d+.\d+)\sGHz")
    QUAL_SLEVEL = re.compile(r"\s+Quality=(\d+/\d+)\s+Signal\slevel=(-?\d+)\sdBm")
    IWLIST_PATH = 'iwlist_path'
    WIFI_IFC= 'wifi_interface'

    def __init__(self, config):
        self.type = "wifi"
        self._config = config
        self._iwlist_path = None
        self._wifi_interface = None
        self._bekende_netwerken = []

    def loaded(self):
        if WifiDevice.IWLIST_PATH in self._config:
            self._iwlist_path = self._config[WifiDevice.IWLIST_PATH]
        else:
            return False
        if WifiDevice.WIFI_IFC in self._config:
            self._wifi_interface = self._config[WifiDevice.WIFI_IFC]
        else:
            return False
        for i in range(1,5):
            wifi_configkey = 'wifi_id_' + str(i)
            if wifi_configkey in self._config:
                self._bekende_netwerken.append(self._config[wifi_configkey])
            else:
                return False
        return True

    def _scan_wifi(self):
        try:
            return subprocess.check_output([self._iwlist_path, self._wifi_interface, 'scanning'], text=True)
        except subprocess.CalledProcessError:
            raise WifiDeviceException("Wifi scan failed.")

    def _get_alle_netwerken(self):
        wifinetwerken = []
        scan = self._scan_wifi()
        wifinetwerk = None
        for line in re.split("\n+", scan):
            if WifiDevice.STARTNETWERK.match(line):
                if wifinetwerk:
                    wifinetwerken.append(wifinetwerk)
                wifinetwerk = WifiNetwerk()
            if wifinetwerk:
                if WifiDevice.CHANNEl.match(line):
                    wifinetwerk.channel = WifiDevice.CHANNEl.match(line).group(1)
                elif WifiDevice.ESSID.match(line):
                    wifinetwerk.essid = WifiDevice.ESSID.match(line).group(1)
                elif WifiDevice.FREQUENCY.match(line):
                    wifinetwerk.frequency_ghz = WifiDevice.FREQUENCY.match(line).group(1)
                elif WifiDevice.QUAL_SLEVEL.match(line):
                    wifinetwerk.quality_percentage = WifiDevice.QUAL_SLEVEL.match(line).group(1)
                    wifinetwerk.signallevel_dbm = WifiDevice.QUAL_SLEVEL.match(line).group(2)
        if wifinetwerk:
            wifinetwerken.append(wifinetwerk)
        return wifinetwerken

    def get_netwerken(self):
        netwerken = []
        for netwerk in self._get_alle_netwerken():
            for bekend_netwerk_id in self._bekende_netwerken:
                if netwerk.essid == bekend_netwerk_id:
                    netwerken.append(netwerk)
        return netwerken
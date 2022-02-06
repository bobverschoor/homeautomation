import unittest

from device.wifi import WifiDevice


class SpyWifi(WifiDevice):
    def _scan_wifi(self):
        with open("wifi_scanning.txt") as f:
            scan = f.read()
        return scan


class TestWifiDevice(unittest.TestCase):
    def test_get_wifinetwerken(self):
        wifidevice = SpyWifi({'iwlist_path': '', 'wifi_interface': ''})
        netwerken = wifidevice._get_alle_netwerken()
        self.assertEqual(36, len(netwerken))
        netwerk = netwerken.pop(0)
        self.assertEqual(8, netwerk.channel)
        self.assertEqual("thuis_zolder", netwerk.essid)
        self.assertEqual(2.447, netwerk.frequency_ghz)
        self.assertEqual(43/70, netwerk.quality_percentage)
        self.assertEqual(-67, netwerk.signallevel_dbm)
        netwerk = netwerken.pop(0)
        self.assertEqual(1, netwerk.channel)
        self.assertEqual("ARLO_VMB_4466787798", netwerk.essid)
        self.assertEqual(2.412, netwerk.frequency_ghz)
        self.assertEqual(43/70, netwerk.quality_percentage)
        self.assertEqual(-67, netwerk.signallevel_dbm)

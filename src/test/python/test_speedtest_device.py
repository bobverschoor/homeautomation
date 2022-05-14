import unittest

from device.sensor.internet_speedtest_device import SpeedtestDevice


class SpeedtestDeviceTest(unittest.TestCase):
    def test_loaded(self):
        st = SpeedtestDevice({})
        self.assertFalse(st.loaded())


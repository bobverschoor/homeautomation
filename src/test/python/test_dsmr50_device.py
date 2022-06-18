import unittest

from device.sensor.dsmr_50_device import DSMR_50, SerialBus
from entiteiten.telegram import TelegramEntityException, Telegram


class Mock_DSMR_50_Device(DSMR_50):

    def __init__(self):
        super().__init__({'p1meter': {'serialport': ''}})
        self._testdata_filename = "../resources/testdata_DSMR_50_Device.txt"

    def read_telegram(self):
        telegram = Telegram()
        with open(self._testdata_filename) as file:
            while line := file.readline().rstrip():
                telegram.add(line)
        return telegram


class MockSerial(SerialBus):
    def __init__(self, p1datafile, p1datafile2=""):
        super().__init__('blah')
        self.p1data = p1datafile
        self.p1data2 = p1datafile2
        self.times_receiving = 0

    def receive_raw_telegram(self):
        p1 = []
        datafile = self.p1data
        if self.times_receiving == 1:
            datafile = self.p1data2
        with open(datafile) as f:
            for l in f.readlines():
                p1.append(l)
        self.times_receiving += 1
        return p1


class DSMR50DeviceTest(unittest.TestCase):
    def test_setup(self):
        self.assertRaises(TelegramEntityException, DSMR_50, {'test': ''})
        self.assertRaises(TelegramEntityException, DSMR_50, {DSMR_50.CONFIG_P1METER: {}})

    def test_read_telegram(self):
        dsmr = DSMR_50({DSMR_50.CONFIG_P1METER: {DSMR_50.CONFIG_SERIALPORT: ''}})
        dsmr.serial = MockSerial('p1data.txt')
        telegram = dsmr.read_telegram()
        self.assertTrue(telegram.is_data_ok())

    def test_read_corrupt_telegram(self):
        dsmr = DSMR_50({DSMR_50.CONFIG_P1METER: {DSMR_50.CONFIG_SERIALPORT: ''}})
        dsmr.serial = MockSerial('p1data_corrupt.txt', 'p1data_corrupt.txt')
        telegram = dsmr.read_telegram()
        self.assertFalse(telegram.is_data_ok())

    def test_read_corrupt_telegram_selfhealing(self):
        dsmr = DSMR_50({DSMR_50.CONFIG_P1METER: {DSMR_50.CONFIG_SERIALPORT: ''}})
        dsmr.serial = MockSerial('p1data_corrupt.txt', 'p1data.txt')
        telegram = dsmr.read_telegram()
        self.assertTrue(telegram.is_data_ok())

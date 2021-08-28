import unittest

from device.deurbel_device import DeurbelKnop, DeurbelGong
from device.raspberrypi import RaspberryPiException, RaspberryPi


class MockRaspberryPi(RaspberryPi):
    def __init__(self):
        super().__init__()
        self.outputValueHighSet = False
        self.outputValueLowSet = False
        self.currentOutputValue = -1
        self.input_value = False

    def is_input_high(self):
        return self.input_value

    def set_output_high(self):
        self.currentOutputValue = True
        self.outputValueHighSet = True

    def set_output_low(self):
        self.currentOutputValue = False
        self.outputValueLowSet = True


class DeurbelDeviceTest(unittest.TestCase):
    def test_deurdevice_exceptions(self):
        self.assertRaises(RaspberryPiException, DeurbelKnop, {'test': ''})
        self.assertRaises(RaspberryPiException, DeurbelKnop, {'gpio_pin_input': 'AA'})
        self.assertRaises(RaspberryPiException, DeurbelGong, {'test': ''})
        self.assertRaises(RaspberryPiException, DeurbelGong, {'gpio_pin_output': 'AA'})

    def test_deurknop_waarde_gelijk_rpi(self):
        self.knop = DeurbelKnop({'gpio_pin_input': 7})
        self.mock_rpi = MockRaspberryPi()
        self.knop._pi = self.mock_rpi
        self.assertFalse(self.knop.is_ingedrukt())
        self.mock_rpi.input_value = True
        self.assertTrue(self.knop.is_ingedrukt())

    def test_deurgong_tenminste_is_ingedrukt_geweest(self):
        # Deurbel klinkt een beperkte tijd, en zal dan altijd uit gaan.
        # Getest door start situatie te vergelijken met eind situatie.
        self.gong = DeurbelGong({'gpio_pin_output': 7})
        self.mock_rpi = MockRaspberryPi()
        self.gong._pi = self.mock_rpi
        self.assertEqual(self.mock_rpi.currentOutputValue, -1)
        self.assertFalse(self.mock_rpi.outputValueHighSet)
        self.assertFalse(self.mock_rpi.outputValueLowSet)
        self.assertRaises(RaspberryPiException, self.gong.ring, duration=15)
        self.gong.ring(duration=0.2)
        self.assertTrue(self.mock_rpi.outputValueHighSet)
        self.assertTrue(self.mock_rpi.outputValueLowSet)
        self.assertFalse(self.mock_rpi.currentOutputValue)


if __name__ == '__main__':
    unittest.main()

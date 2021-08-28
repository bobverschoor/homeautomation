import unittest
from device.raspberrypi import RaspberryPi, RaspberryPiException


class MockGpio:
    PUD_DOWN = 1
    BOARD = 1
    IN = 1
    OUT = 2
    HIGH = 1
    LOW = 0

    def __init__(self):
        self.IN = ""
        self.OUT = ""
        self.input_waarde = -1
        self.pin = {}

    def setup(self, pin, io, pull_up_down="PUD_DOWN"):
        self.pin[pin] = -1

    def input(self, input):
        return self.input_waarde

    def output(self, pin, waarde):
        self.pin[pin] = waarde


class RaspberryPiTest(unittest.TestCase):

    def setUp(self):
        self.rpi = RaspberryPi()
        self.mockgpio = MockGpio()
        self.rpi._gpio = self.mockgpio

    def test_rpisetupthrowsexception(self):
        self.assertRaises(RaspberryPiException, self.rpi.setup_inputpin, 100)
        self.assertRaises(RaspberryPiException, self.rpi.setup_outputpin, 100)
        self.assertFalse(self.rpi.is_input_setup())
        self.assertFalse(self.rpi.is_output_setup())

    def test_rpi_isinput_high(self):
        self.assertRaises(RaspberryPiException, self.rpi.is_input_high)
        self.rpi.setup_inputpin(8)
        self.assertTrue(self.rpi.is_input_setup())
        self.assertEqual(self.rpi._input_pin, 8)
        self.rpi._gpio.input_waarde = 1
        self.assertTrue(self.rpi.is_input_high())

    def test_rpi_output(self):
        self.assertRaises(RaspberryPiException, self.rpi.set_output_low)
        self.assertRaises(RaspberryPiException, self.rpi.set_output_high)
        self.rpi.setup_outputpin(7)
        self.assertTrue(self.rpi.is_output_setup())
        self.rpi.set_output_low()
        self.assertEqual(self.mockgpio.pin[7], False)
        self.rpi.set_output_high()
        self.assertEqual(self.mockgpio.pin[7], True)


if __name__ == '__main__':
    unittest.main()

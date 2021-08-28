try:
    import RPi.GPIO as GPIO
except ImportError:
    import device.RPi_dev.GPIO as GPIO


class RaspberryPiException(Exception):
    def __init__(self, message):
        super(RaspberryPiException, self).__init__(message)


class RaspberryPi:
    VALID_CHANNELS = [3,5,7,8,10,11,12,13,15,16,18,19,21,22,23,24,26,27,28,29,31,32,33,35,36,37,38,40]

    def __init__(self):
        self._gpio = GPIO
        self._gpio.setmode(GPIO.BOARD)
        self._gpio.setwarnings(False)
        self._input_pin = -1
        self._output_pin = -1

    def is_input_setup(self):
        return self._input_pin != -1

    def is_output_setup(self):
        return self._output_pin != -1

    def setup_inputpin(self, pin_nummer):
        channel = int(pin_nummer)
        if channel in RaspberryPi.VALID_CHANNELS:
            self._gpio.setup(channel, self._gpio.IN, pull_up_down=self._gpio.PUD_DOWN)
            self._input_pin = channel
        else:
            raise RaspberryPiException("Pin nummer wrong: " + str(pin_nummer))

    def setup_outputpin(self, pin_nummer):
        channel = int(pin_nummer)
        if channel in RaspberryPi.VALID_CHANNELS:
            self._gpio.setup(channel, GPIO.OUT)
            self._output_pin = channel
        else:
            raise RaspberryPiException("Pin nummer wrong: " + str(pin_nummer))

    def is_input_high(self):
        if self._input_pin == -1:
            raise RaspberryPiException("Input pin not setup")
        return self._gpio.input(self._input_pin) == self._gpio.HIGH

    def set_output_high(self):
        if self._output_pin == -1:
            raise RaspberryPiException("Output pin not setup")
        self._gpio.output(self._output_pin, True)

    def set_output_low(self):
        if self._output_pin == -1:
            raise RaspberryPiException("Output pin not setup")
        self._gpio.output(self._output_pin, False)

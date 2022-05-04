from device.raspberrypi import RaspberryPi, RaspberryPiException
import time


class DeurbelKnop:
    CONFIG_GPIO_INPUT = 'gpio_pin_input'
    CONFIG_GPIO_OUTPUT = 'gpio_pin_output'

    def __init__(self, config):
        self._pi = RaspberryPi()
        if DeurbelKnop.CONFIG_GPIO_INPUT in config:
            try:
                self._pinnummer = int(config[DeurbelKnop.CONFIG_GPIO_INPUT])
            except ValueError:
                raise RaspberryPiException('Config: ' + DeurbelKnop.CONFIG_GPIO_INPUT + ' value is not an integer')
        else:
            raise RaspberryPiException('Config: Missing ' + DeurbelKnop.CONFIG_GPIO_INPUT)

    def is_ingedrukt(self):
        if not self._pi.is_input_setup():
            self._pi.setup_inputpin(self._pinnummer)
        return self._pi.is_input_high()


class DeurbelGong:
    def __init__(self, config):
        self._pi = RaspberryPi()
        if DeurbelKnop.CONFIG_GPIO_OUTPUT in config:
            try:
                self._pinnummer = int(config[DeurbelKnop.CONFIG_GPIO_OUTPUT])
            except ValueError:
                raise RaspberryPiException('Config: ' + DeurbelKnop.CONFIG_GPIO_OUTPUT + ' value is not an integer')
        else:
            raise RaspberryPiException('Config: Missing ' + DeurbelKnop.CONFIG_GPIO_OUTPUT)
        self.stil()

    def ring(self, duration=1):
        if duration > 10 or duration < 0.1:
            raise RaspberryPiException("duration too long: " + str(duration))
        try:
            if not self._pi.is_output_setup():
                self._pi.setup_outputpin(self._pinnummer)
            self._pi.set_output_high()
            time.sleep(duration)
        finally:
            self.stil()

    def stil(self):
        if not self._pi.is_output_setup():
            self._pi.setup_outputpin(self._pinnummer)
        self._pi.set_output_low()

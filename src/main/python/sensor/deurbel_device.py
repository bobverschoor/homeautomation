from sensor.raspberrypi import RaspberryPi
import time

class DeurbelKnop:
    def __init__(self, pinnummer):
        self._pi = RaspberryPi()
        self._pinnummer = pinnummer

    def is_ingedrukt(self):
        if not self._pi.is_input_setup():
            self._pi.setup_inputpin(self._pinnummer)
        return self._pi.is_input_high()


class DeurbelGong:
    def __init__(self, pinnummer):
        self._pi = RaspberryPi()
        self._pinnummer = pinnummer

    def ring(self, duration=0.5):
        if 0.1 > duration > 10:
            print("duration too long: " + str(duration))
            duration = 0.5
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

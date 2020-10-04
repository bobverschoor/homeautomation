import json

from sensor.p1_device import P1Device


class MockP1Device(P1Device):
    def __init__(self, file):
        self.file = file

    def get_data(self):
        with open(self.file) as json_file:
            data = json.load(json_file)
        return data



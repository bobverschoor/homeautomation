from persistence.influxdb_device import InFluxDBDevice


class MockInFluxDBDevice(InFluxDBDevice):
    # noinspection PyMissingConstructor
    def __init__(self):
        self._meetwaarde = None

    def write(self, meetwaarde):
        self._meetwaarde = meetwaarde

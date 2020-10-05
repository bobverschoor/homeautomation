from persistence.influxdb_device import InFluxDBDevice


class DatabaseGateway:
    def __init__(self):
        self.repository = InFluxDBDevice()
        self.entiteiten = []

    def store(self):
        for entiteit in self.entiteiten:
            self.repository.write(entiteit)

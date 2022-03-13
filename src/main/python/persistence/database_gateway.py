from persistence.influxdb_device import InFluxDBDevice


class DatabaseGateway:
    def __init__(self, databasenaam):
        self.repository = None
        self._databasenaam = databasenaam
        self._entiteiten = []

    @property
    def entiteiten(self):
        return self._entiteiten

    @entiteiten.setter
    def entiteiten(self, new_entiteit):
        double = False
        for entiteit in self.entiteiten:
            if entiteit == new_entiteit:
                double = True
        if not double:
            self._entiteiten.append(new_entiteit)

    def get_db_entiteiten(self):
        db_entiteiten = []
        for entiteit in self.entiteiten:
            db_entiteit = {
                "measurement": entiteit.eenheid,
                "tags": entiteit.tags,
                "time": entiteit.timestamp,
                "fields": {"meetwaarde": entiteit.waarde}
            }
            db_entiteiten.append(db_entiteit)
        return db_entiteiten

    def store(self):
        if not self.repository:
            self.repository = InFluxDBDevice(self._databasenaam)
        self.repository.write(self.get_db_entiteiten())

    def print(self):
        for entiteit in self.get_db_entiteiten():
            print(entiteit)

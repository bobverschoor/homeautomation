from persistence.influxdb_device import InFluxDBDevice


class DatabaseGateway:
    def __init__(self):
        self.repository = InFluxDBDevice()
        self.entiteiten = []

    def store(self):
        self.repository.setup_db()
        db_entiteiten = []
        for entiteit in self.entiteiten:
            db_entiteit = {
                "measurement": entiteit.eenheid,
                "tags": entiteit.tags,
                "time": entiteit.timestamp,
                "fields": {"meetwaarde": entiteit.waarde}
                }
            db_entiteiten.append(db_entiteit)
        self.repository.write(db_entiteiten)

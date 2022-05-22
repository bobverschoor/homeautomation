class DatabaseGatewayException(Exception):
    def __init__(self, message):
        super(DatabaseGatewayException, self).__init__(message)


class DatabaseGateway:
    def __init__(self, database_device=None):
        self.repository = database_device
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
            raise DatabaseGatewayException("Database device not coupled")
        self.repository.write(self.get_db_entiteiten())

    def __str__(self):
        out = ""
        for entiteit in self.get_db_entiteiten():
            out = out + "\n" + "meetwaarde: " + str(entiteit["fields"]["meetwaarde"]) + \
                  " (" + str(entiteit["measurement"]) + "), tags:" + str(entiteit["tags"]) + ", time:" + \
                  str(entiteit["time"])
        return out

from persistence.database_gateway import DatabaseGateway
from sensor.slimmemeter_gateway import SlimmemeterGateway


class Verlader:
    def __init__(self):
        self.slimmemeter = SlimmemeterGateway()
        self.database = DatabaseGateway()
        self.metingen = []

    def collect(self):
        for electra in self.slimmemeter.electra:
            self.metingen.append(electra)
        for gas in self.slimmemeter.gas:
            self.metingen.append(gas)

    def store(self):
        self.database.entiteiten = self.metingen
        self.database.store()
        self.metingen = []

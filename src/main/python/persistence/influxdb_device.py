from influxdb import InfluxDBClient


class InFluxDBDevice:
    DB_Naam = "p1meter"

    def __init__(self):
        self.client = None
        self.database = None

    def setup_db(self):
        if self.client is None:
            self.client = InfluxDBClient('localhost', 8086)
        if self.database is None:
            if InFluxDBDevice.DB_Naam not in self.client.get_list_database():
                self.client.create_database(InFluxDBDevice.DB_Naam)

    def write(self, meetwaarde):
        if not self.client.write_points(meetwaarde):
            raise IOError(f"writeing: {str(meetwaarde)} to database failed.")

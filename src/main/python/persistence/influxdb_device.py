from influxdb import InfluxDBClient


class InFluxDBDevice:
    DB_Naam = "p1meter"

    def __init__(self):
        self.db_host = 'localhost'
        self.db_port = 8086
        self.db_name = InFluxDBDevice.DB_Naam

    def write(self, meetwaarde):
        client = InfluxDBClient(host=self.db_host, port=self.db_port, database=self.db_name)
        # Apparently cheaper to just try to create db even if it exists.
        client.create_database(InFluxDBDevice.DB_Naam)
        client.switch_database(InFluxDBDevice.DB_Naam)
        if not client.write_points(meetwaarde, time_precision='s'):
            client.close()
            raise IOError(f"writeing: {str(meetwaarde)} to database failed.")
        client.close()

    def drop_database(self):
        client = InfluxDBClient(host=self.db_host, port=self.db_port, database=self.db_name)
        # Apparently cheaper to just try to create db even if it exists.
        client.drop_database(InFluxDBDevice.DB_Naam)

    def get_all_items(self):
        client = InfluxDBClient(host=self.db_host, port=self.db_port, database=self.db_name)
        client.switch_database(InFluxDBDevice.DB_Naam)
        return list(client.query("SELECT * from " + self.db_name).get_points())
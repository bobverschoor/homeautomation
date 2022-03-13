from influxdb import InfluxDBClient


class InFluxDBDevice:

    def __init__(self, databasenaam):
        self.db_host = 'localhost'
        self.db_port = 8086
        self.db_name = databasenaam

    def write(self, meetwaarde):
        client = InfluxDBClient(host=self.db_host, port=self.db_port, database=self.db_name)
        # Apparently cheaper to just try to create db even if it exists.
        client.create_database(self.db_name)
        client.switch_database(self.db_name)
        if not client.write_points(meetwaarde, time_precision='s'):
            client.close()
            raise IOError(f"writeing: {str(meetwaarde)} to database failed.")
        client.close()

    def drop_database(self):
        client = InfluxDBClient(host=self.db_host, port=self.db_port, database=self.db_name)
        # Apparently cheaper to just try to create db even if it exists.
        client.drop_database(self.db_name)

    def get_all_items(self):
        client = InfluxDBClient(host=self.db_host, port=self.db_port, database=self.db_name)
        client.switch_database(self.db_name)
        return list(client.query("SELECT * from " + self.db_name).get_points())

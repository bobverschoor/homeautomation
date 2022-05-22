from influxdb import InfluxDBClient


class InFluxDBDevice:

    def __init__(self, databasenaam, hostname='localhost', port=8086):
        self.db_host = hostname
        self.db_port = port
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

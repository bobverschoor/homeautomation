from sensor.api import Api


class WeerhuisjeDevice:
    WEERHUISJE_BASE_URL = 'https://www.mijneigenweer.nl/'

    def __init__(self, config):
        self._locatie1 = config['weerhuisje']['locatie_1']
        self.api = None

    def set_api(self):
        payload = {}
        url = self.WEERHUISJE_BASE_URL + self._locatie1 + "/MBrealtimegauges.txt"
        self.api = Api(url, payload)

    def get_neerslaghoeveelheid(self):
        hoeveelheid = -1
        if not self.api:
            self.set_api()
        self.api.request_data()
        weer = self.api.get_json()
        if 'rfall' in weer:
            hoeveelheid = float(weer['rfall'])
        return hoeveelheid

    @property
    def locatie(self):
        return self._locatie1
#        for neerslagtijden in self.api.text_output():


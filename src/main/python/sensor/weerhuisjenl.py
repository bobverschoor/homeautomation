from sensor.api import Api


class WeerhuisjeDevice:
    WEERHUISJE_BASE_URL = 'https://www.mijneigenweer.nl/'

    def __init__(self, config):
        self._locatie1 = config['weer']['weerhuisje_locatie_1']
        self.api = None

    def set_api(self):
        payload = {}
        url = self.WEERHUISJE_BASE_URL + self._locatie1 + "/MBrealtimegauges.txt"
        self.api = Api(url, payload)

    def extend_weerentiteit(self, weer):
        if not self.api:
            self.set_api()
        self.api.request_data()
        weerdata = self.api.get_json()
        if 'rfall' in weerdata:
            weer.neerslaghoeveelheid24h = weerdata['rfall']
            weer.set_locatie_for_meting("neerslaghoeveelheid24h", self._locatie1)
        else:
            weer.error = "Geen rfall in API:\n" + str(weerdata)
        if 'rrate' in weerdata:
            weer.neerslagintensiteit = weerdata['rrate']
            weer.set_locatie_for_meting("neerslagintensiteit", self._locatie1)
        else:
            weer.error = "Geen rrate in API:\n" + str(weerdata)
        return weer

    @property
    def locatie(self):
        return self._locatie1


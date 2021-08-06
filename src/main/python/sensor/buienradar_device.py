from sensor.api import Api


class BuienradarDevice:
    BUIENRADAR_BASE_URL = 'https://gpsgadget.buienradar.nl/data/raintext/'

    def __init__(self, config):
        self._latitude = config['buienradar']['latitude']
        self._longitude = config['buienradar']['longitude']
        self.api = None

    def set_api(self):
        payload = {'lat':self._latitude, 'lon':self._longitude}
        self.api = Api(BuienradarDevice.BUIENRADAR_BASE_URL, payload)

    def get_neerslag(self):
        if not self.api:
            self.set_api()
        self.api.request_data()
        print(self.api.get_text_output())
#        for neerslagtijden in self.api.text_output():


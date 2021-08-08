from sensor.api import Api


class WeerLiveDevice:
    WEERLIVE_BASE_URL = 'https://weerlive.nl/api/json-data-10min.php'

    def __init__(self, config):
        self._api_key = config['weerlive']['api_key']
        self._locatie = config['weerlive']['locatie']
        self.api = None

    def set_api(self):
        payload = {'key': self._api_key, 'locatie': self._locatie}
        self.api = Api(WeerLiveDevice.WEERLIVE_BASE_URL, payload)

    def extend_weerentiteit(self, weer):
        if not self.api:
            self.set_api()
        self.api.request_data()
        weerlivedata = self.api.get_json()
        if "liveweer" in weerlivedata:
            weerlivedata = weerlivedata["liveweer"]
            weerlivedata = weerlivedata[0]
            for weermeting in weerlivedata.keys():
                if weermeting == 'temp':
                    weer.temperatuur = weerlivedata[weermeting]
                elif weermeting == 'plaats':
                    weer.locatie = weerlivedata[weermeting]
                elif weermeting == 'gtemp':
                    weer.gevoelstemperatuur = weerlivedata[weermeting]
                elif weermeting == 'windr':
                    weer.windrichting = weerlivedata[weermeting]
                elif weermeting == 'windms':
                    weer.windsnelheidms = weerlivedata[weermeting]
                elif weermeting == 'lv':
                    weer.luchtvochtigheid = weerlivedata[weermeting]
                elif weermeting == 'luchtd':
                    weer.luchtdruk = weerlivedata[weermeting]
        else:
            weer.error = "Weerdata ongeldig: " + str(weerlivedata)
        return weer

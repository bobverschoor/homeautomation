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
            if 'plaats' in weerlivedata:
                locatie = weerlivedata['plaats']
            else:
                locatie = self._locatie
            for weermeting in weerlivedata.keys():
                if weermeting == 'temp':
                    weer.temperatuur = weerlivedata[weermeting]
                    weer.set_locatie_for_meting("temperatuur", locatie)
                elif weermeting == 'gtemp':
                    weer.gevoelstemperatuur = weerlivedata[weermeting]
                    weer.set_locatie_for_meting("gevoelstemperatuur", locatie)
                elif weermeting == 'windr':
                    weer.windrichting = weerlivedata[weermeting]
                    weer.set_locatie_for_meting("windrichting", locatie)
                elif weermeting == 'windms':
                    weer.windsnelheidms = weerlivedata[weermeting]
                    weer.set_locatie_for_meting("windsnelheidms", locatie)
                elif weermeting == 'lv':
                    weer.luchtvochtigheid = weerlivedata[weermeting]
                    weer.set_locatie_for_meting("luchtvochtigheid", locatie)
                elif weermeting == 'luchtd':
                    weer.luchtdruk = weerlivedata[weermeting]
                    weer.set_locatie_for_meting("luchtdruk", locatie)
        else:
            weer.error = "Weerdata ongeldig: " + str(weerlivedata)
        return weer

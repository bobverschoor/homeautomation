from device.api import Api
from entiteiten.licht import Licht


class HueBridgeException(Exception):
    def __init__(self, message):
        super(HueBridgeException, self).__init__(message)


class HueBridgeDevice:
    CONFIG_HUEBRIDGE = 'hue'
    CONFIG_IP = 'ipadress'
    CONFIG_USERNAME = 'username'

    def __init__(self, config):
        if HueBridgeDevice.CONFIG_HUEBRIDGE in config:
            config = config[HueBridgeDevice.CONFIG_HUEBRIDGE]
            if HueBridgeDevice.CONFIG_IP in config:
                self._ipadress = config[HueBridgeDevice.CONFIG_IP]
            else:
                raise HueBridgeException("Config section [" + HueBridgeDevice.CONFIG_HUEBRIDGE + "] missing " +
                                         HueBridgeDevice.CONFIG_IP)
            if HueBridgeDevice.CONFIG_USERNAME in config:
                self._api_key = config[HueBridgeDevice.CONFIG_USERNAME]
            else:
                raise HueBridgeException("Config section [" + HueBridgeDevice.CONFIG_HUEBRIDGE + "] missing " +
                                         HueBridgeDevice.CONFIG_USERNAME)
        else:
            raise HueBridgeException("Config section [" + HueBridgeDevice.CONFIG_HUEBRIDGE + "] missing ")
        self._getlights_api = Api("http://" + self._ipadress + "/api/" + self._api_key + "/lights")

    def get_alle_lichten(self):
        lichten = []
        self._getlights_api.request_data()
        light = self._getlights_api.get_json()
        for volgnr in light.keys():
            licht = Licht(volgnr)
            licht.naam = light[volgnr]['name']
            if light[volgnr]['state']['reachable']:
                licht.aan = light[volgnr]['state']['on']
            else:
                licht.aan = False
            licht.unique_id = light[volgnr]['uniqueid']
            lichten.append(licht)
        return lichten

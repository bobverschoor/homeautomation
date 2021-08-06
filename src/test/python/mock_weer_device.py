from entiteiten.weer import Weer
from sensor.weerhuisjenl import WeerhuisjeDevice
from sensor.weerlive_api import WeerLiveDevice


class MockWeerLiveDevice(WeerLiveDevice):
    def __init__(self):
        super().__init__({'weerlive':{'api_key':"", 'locatie':""}})
        self.weer = Weer()

    def get_weerentiteit(self):
        return self.weer


class MockWeerhuisjeDevice(WeerhuisjeDevice):
    def __init__(self):
        super().__init__({'weerhuisje':{'locatie_1':"weerstationwijkaanzee"}})

    def get_neerslaghoeveelheid(self):
        return 2.1
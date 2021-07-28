from entiteiten.weer import Weer
from sensor.weerlive_api import WeerLiveDevice


class MockWeerLiveDevice(WeerLiveDevice):
    def __init__(self):
        super().__init__({'weerlive':{'api_key':"", 'locatie':""}})
        self.weer = Weer()

    def get_weerentiteit(self):
        return self.weer

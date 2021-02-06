from entiteiten.electra import Electra
from entiteiten.gas import Gas
from sensor.p1_device import P1Device
import json

class SlimmemeterGateway:
    def __init__(self):
        self.p1 = None
        self._electra = []
        self._gas = []

    @property
    def electra(self):
        if not self._electra:
            self._collect_data()
        return self._electra

    @property
    def gas(self):
        if not self._gas:
            self._collect_data()
        return self._gas

    def set_p1(self, device):
        self.p1 = device

    def _collect_data(self):
        if self.p1 is None:
            raise ModuleNotFoundError("p1 device not set")
        data = json.loads(self.p1.get_data())
        self._set_electra(data['electra'])
        self._set_gas(data['gas'])

    def _set_electra(self, electra):
        for tarief in electra.keys():
            for richting in electra[tarief]:
                e = Electra()
                e.waarde = int(electra[tarief][richting] * 1000)
                if tarief == P1Device.E_LAAG:
                    e.tarief = Electra.LAAGTARIEF
                else:
                    e.tarief = Electra.HOOGTARIEF
                if richting == P1Device.E_PRODUCED:
                    e.richting = Electra.GELEVERD
                else:
                    e.richting = Electra.VERBRUIKT
                self._electra.append(e)

    def _set_gas(self, gas):
        g = Gas()
        g.timestamp = gas["timestamp"]
        g.waarde = gas["m3"]
        self._gas.append(g)
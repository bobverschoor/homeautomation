from entiteiten.electra import Electra
from entiteiten.gas import Gas
from entiteiten.meetwaarde import Meetwaarde
from entiteiten.slimmemeter import Slimmemeter
from sensor.p1_device import P1Device
import json


class SlimmemeterGateway:
    def __init__(self):
        self.p1 = None
        self._electra = []
        self._gas = []
        self._slimmemeter = None

    def get_meetwaarden(self):
        if self.p1 is None:
            raise ModuleNotFoundError("p1 device not set")
        telegram = self.p1.read_telegram()
        meetwaardes = []
        for property_name, value in telegram.get_properties():
            if value != "" and property_name not in ["version", "meter_id", "timestamp"]:
                timestamp = telegram.timestamp
                meter_id = telegram.meter_id
                if type(value) is tuple:
                    if len(value) == 2:
                        waarde, v2 = value
                    else:
                        timestamp, meter_id, waarde, v2 = value
                else:
                    waarde = value
                    v2 = "aantal"
                if type(waarde) in [int, float]:
                    meetwaarde = Meetwaarde(v2)
                    meetwaarde.slimmemeter = Slimmemeter(telegram.manufacture)
                    meetwaarde.tags = "meterid:" + str(meter_id)
                    if property_name == "gasmeter":
                        meetwaarde.tags = "soort:gasmeterstand"
                    else:
                        for tag in get_tags_from_property_name(property_name):
                            meetwaarde.tags = tag
                    meetwaarde.waarde = waarde
                    meetwaarde.timestamp = timestamp
                    meetwaardes.append(meetwaarde)
        return meetwaardes

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
        self._slimmemeter = Slimmemeter(data['header'])
        self._set_electra(data['electra'])
        self._set_gas(data['gas'])
        for e in self._electra:
            e.slimmemeter = self._slimmemeter

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
        g.slimmemeter = self._slimmemeter
        self._gas.append(g)


def get_tags_from_property_name(prop):
    tags = []
    for part in prop.split('_'):
        tag = ""
        if part == 'consumed':
            tag = "richting:" + Electra.VERBRUIKT
            tags.append(tag)
        elif part == 'produced':
            tag = "richting:" + Electra.GELEVERD
        elif part == 'tariff1':
            tag = "tarief:laag"
        elif part == 'tariff2':
            tag = "tarief:hoog"
        elif part == 'actualpower':
            tag = "soort:actueel_vermogen"
        elif part == 'meterstandelectra':
            tag = "soort:meterstand_electra"
        elif part == "aantaltelagespanning":
            tag = "soort:aantal_te_lage_spanning"
        elif part == "aantaltehogespanning":
            tag = "soort:aantal_te_hoge_spanning"
        elif part == "instantaneousvoltage":
            tag = "soort:momentane_spanning"
        elif part == "instantaneouscurrent":
            tag = "soort:momentane_stroom"
        elif part == "instantaneouspower":
            tag = "soort:momentane_vermogen"
        elif part == "aantalstoringen":
            tag = "soort:aantal_storingen"
        elif part == "aantallangdurigestoringen":
            tag = "soort:aantal_langdurige_storingen"
        elif part.startswith('l') and len(part) == 2:
            tag = "fase:" + part[1]
        if tag == "":
            print("skipped: " + part)
        else:
            tags.append(tag)
    return tags

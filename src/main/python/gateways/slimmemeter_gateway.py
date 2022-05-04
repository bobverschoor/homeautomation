from entiteiten.electra import Electra
from entiteiten.meetwaarde import Meetwaarde, convertlist2tags


def get_meternaam_metertype_from_manufacture(manufacture):
    meternaam = ""
    metertype = ""
    manufacture = manufacture.strip()
    manufacture = manufacture.strip('//')
    if manufacture == "":
        print("manufacture is empty")
    else:
        try:
            meternaam, metertype = manufacture.split('\\')
        except ValueError:
            print("manufacture of wrong format:" + str(manufacture))
    return meternaam, metertype


class SlimmemeterGateway:
    def __init__(self):
        self.p1 = None

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
                    meternaam, metertype = get_meternaam_metertype_from_manufacture(telegram.manufacture)
                    tags = ["meternaam:" + meternaam, "metertype:" + metertype, "meterid:" + str(meter_id)]
                    if property_name == "gasmeter":
                        tags.append("soort:gasmeterstand")
                    else:
                        for tag in get_tags_from_property_name(property_name):
                            tags.append(tag)
                    meetwaarde = Meetwaarde(waarde=waarde, eenheid=v2, timestamp=timestamp, tags=convertlist2tags(tags))
                    meetwaardes.append(meetwaarde)
        return meetwaardes

    def set_p1(self, device):
        self.p1 = device


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

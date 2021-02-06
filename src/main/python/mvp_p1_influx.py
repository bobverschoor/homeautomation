#[{"measurement": "h2o_feet", "tags": {"location": "coyote_creek"},
#"fields": {"water_level": 2.0}, "time": 2},
#{"measurement": "h2o_feet", "tags": {"location": "coyote_creek"},
#"fields": {"water_level": 3.0}, "time": 3}])

# datastr = '{"electra": {"low": {"consumed": 17069.223, "produced": 1.804}, ' \
#        '"high": {"consumed": 21100.748, "produced": 0.007}},' \
#        '"gas": {"m3": 7368.67, "timestamp": 1612623600}}'

from sensor.slimmemeter_gateway import SlimmemeterGateway
from sensor.p1_device import P1Device
import datetime
import json

#data = json.loads(datastr)

slimmemeter = SlimmemeterGateway()
slimmemeter.set_p1(P1Device())


# measurement: electra, tags: {low, consumed}, fields: {"kwh":17069.223, "time":now}
#measurement: gas, fields: {"m3":7368.67, "timestamp": 1612623600}

metingen = []

for electra in slimmemeter.electra:
    meting = {}
    meting["measurement"] = "electra"
    meting["tags"] = {}
    meting["fields"] = {}
    meting["tags"]["tarief"] = electra.tarief
    meting["tags"]["richting"] = electra.richting
    meting["fields"]["kwh"] = electra.waarde
    meting["fields"]["timestamp"] = electra.timestamp
    metingen.append(meting)

for gas in slimmemeter.gas:
    meting = {}
    meting["measurement"] = "gas"
    meting["fields"] = {}
    meting["fields"]["m3"] = gas.waarde
    meting["fields"]["timestamp"] = gas.timestamp
    metingen.append(meting)

print(metingen)

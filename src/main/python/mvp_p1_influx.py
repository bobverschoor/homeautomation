#[{"measurement": "h2o_feet", "tags": {"location": "coyote_creek"},
#"fields": {"water_level": 2.0}, "time": 2},
#{"measurement": "h2o_feet", "tags": {"location": "coyote_creek"},
#"fields": {"water_level": 3.0}, "time": 3}])

# {"electra": {"low": {"consumed": 17069.223, "produced": 1.804},
#              "high": {"consumed": 21100.748, "produced": 0.007}},
#  "gas": {"m3": 7368.67, "timestamp": 1612623600}}

from sensor.p1_device import P1Device
import datetime

p1 = P1Device()
data = p1.get_data()

# measurement: electra, tags: {low, consumed}, fields: {"kwh":17069.223, "time":now}
#measurement: gas, fields: {"m3":7368.67, "timestamp": 1612623600}

metingen = []
meting = {}
meting["measurement"] = "electra"
for lh in data["electra"].keys():
    meting["tags"] = {}
    meting["fields"] = {}
    meting["tags"]["tarief"] = lh
    for richting in data["electra"][lh].keys():
        meting["tags"]["richting"] = richting
        meting["fields"]["kwh"] = data["electra"]
        meting["fields"]["timestamp"] = str(datetime.datetime.now())
metingen.append(meting)
meting["measurement"] = "gas"
meting["fields"] = {}
meting["fields"]["m3"] = data["gas"]["m3"]
meting["fields"]["timestamp"] = data["gas"]["timestamp"]
metingen.append(meting)

print(metingen)

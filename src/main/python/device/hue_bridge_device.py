import json
import threading
import time

from device.api import Api
from entiteiten.licht import Licht
from entiteiten.sensor import Schakelaar, BewegingSchakelaar, TemperatuurSensor, LichtSensor


class HueBridgeException(Exception):
    def __init__(self, message):
        super(HueBridgeException, self).__init__(message)


class HueBridgeDevice:
    CONFIG_HUEBRIDGE = 'hue'
    CONFIG_IP = 'ipadress'
    CONFIG_USERNAME = 'username'
    CONFIG_ALERTTIMES = 'aantal_keer_knipperen_per_alarm'
    CONFIG_ALERTGROUP = 'alarmeer_groepnaam'
    DEFAULT_ALERTTIMES = 5
    WAIT_SECS = 0.5 # is minimale waarde voor knipperen

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
            if HueBridgeDevice.CONFIG_ALERTGROUP in config:
                self._alertgroupname = config[HueBridgeDevice.CONFIG_ALERTGROUP]
            else:
                raise HueBridgeException("Config section [" + HueBridgeDevice.CONFIG_HUEBRIDGE + "] missing " +
                                         HueBridgeDevice.CONFIG_ALERTGROUP)
            if HueBridgeDevice.CONFIG_ALERTTIMES in config:
                self._nr_of_alert = config[HueBridgeDevice.CONFIG_ALERTTIMES]
            else:
                self._nr_of_alert = 5
        else:
            raise HueBridgeException("Config section [" + HueBridgeDevice.CONFIG_HUEBRIDGE + "] missing ")
        self._lichts_api = Api("http://" + self._ipadress + "/api/" + self._api_key + "/lights",
                               expected_startsymbol="")
        self._groups_api = Api("http://" + self._ipadress + "/api/" + self._api_key + "/groups")
        self._sensors_api = Api("http://" + self._ipadress + "/api/" + self._api_key + "/sensors")

    def get_alle_lichten(self):
        lichten = []
        self._lichts_api.request_data()
        light = self._lichts_api.get_json()
        for volgnr in light.keys():
            licht = Licht(volgnr)
            licht.naam = light[volgnr]['name']
            licht.bereikbaar = light[volgnr]['state']['reachable']
            if licht.bereikbaar:
                licht.aan = light[volgnr]['state']['on']
            else:
                licht.aan = False
            licht.unique_id = light[volgnr]['uniqueid']
            lichten.append(licht)
        return lichten

    def get_alle_sensors(self):
        sensors = []
        self._sensors_api.request_data()
        sensors_json = self._sensors_api.get_json()
        for volgnr in sensors_json.keys():
            sensor_json = sensors_json[volgnr]
            sensor_state = sensor_json['state']
            sensor_config = sensor_json['config']
            if sensor_json['type'] == 'ZLLSwitch':
                sensor = Schakelaar(volgnr)
                sensor.knop_id = sensor_state['buttonevent']
            elif sensor_json['type'] == 'ZLLPresence':
                sensor = BewegingSchakelaar(volgnr)
                sensor.beweging_gesignaleerd = sensor_state['presence']
            elif sensor_json['type'] == 'ZLLTemperature':
                sensor = TemperatuurSensor(volgnr)
                sensor.temperature = sensor_state['temperature']
            elif sensor_json['type'] == 'ZLLLightLevel':
                sensor = LichtSensor(volgnr)
                sensor.lichtniveau = sensor_state['lightlevel']
            else:
                continue
            sensor.naam = sensor_json['name']
            sensor.unique_id = sensor_json['uniqueid']
            sensor.bereikbaar = sensor_config['reachable']
            sensor.batterijpercentage = sensor_config['battery']
            sensor.tijdstip_meting = sensor_state['lastupdated']
            sensors.append(sensor)
        return sensors

    def get_alle_lichten_in_alarmeergroep(self):
        lichten = []
        self._groups_api.request_data()
        group = self._groups_api.get_json()
        gevondengroep = None
        for groupnr in group.keys():
            groep = group[groupnr]
            if groep['name'] == self._alertgroupname:
                gevondengroep = groep
                break
        if gevondengroep:
            alle_lichten = self.get_alle_lichten()
            for licht_volgnr in gevondengroep['lights']:
                for licht in alle_lichten:
                    if licht.volgnr == int(licht_volgnr):
                        lichten.append(licht)
        return lichten

    def alerting(self, lichten):
        body = {}
        alert = 1
        while alert <= self._nr_of_alert:
            body["alert"] = "select"
            for licht in lichten:
                self._lichts_api.put_data(json.dumps(body), additionalpath="/" + str(licht.volgnr) + "/state")
            time.sleep(HueBridgeDevice.WAIT_SECS)
            alert += 1
        for licht in lichten:
            body["alert"] = "none"
            self._lichts_api.put_data(json.dumps(body), additionalpath="/" + str(licht.volgnr) + "/state")

    def alert_lights(self, lichten):
        t = threading.Thread(target=self.alerting, args=[lichten])
        t.setDaemon(True)
        t.start()

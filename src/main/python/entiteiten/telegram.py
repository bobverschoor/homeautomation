import re
import datetime
import inspect


def obis2attribute(obis):
    if obis == '1-3:0.2.8':
        return 'version'
    elif obis == '0-0:1.0.0':
        return 'timestamp'
    elif obis == '0-0:96.1.1':
        return 'meter_id'
    elif obis == '1-0:1.8.1':
        return 'meterstandelectra_consumed_tariff1'
    elif obis == '1-0:1.8.2':
        return 'meterstandelectra_consumed_tariff2'
    elif obis == '1-0:2.8.1':
        return 'meterstandelectra_produced_tariff1'
    elif obis == '1-0:2.8.2':
        return 'meterstandelectra_produced_tariff2'
    elif obis == '0-0:96.14.0':
        return 'current_tariff'
    elif obis == '1-0:1.7.0':
        return 'actualpower_consumed'
    elif obis == '1-0:2.7.0':
        return 'actualpower_produced'
    elif obis == '0-0:96.7.21':
        return 'aantalstoringen'
    elif obis == '0-0:96.7.9':
        return 'aantallangdurigestoringen'
    elif obis == '1-0:99.97.0':
        return 'power_failure_events'
    elif obis == '1-0:32.32.0':
        return 'aantaltelagespanning_l1'
    elif obis == '1-0:52.32.0':
        return 'aantaltelagespanning_l2'
    elif obis == '1-0:72.32.0':
        return 'aantaltelagespanning_l3'
    elif obis == '1-0:32.36.0':
        return 'aantaltehogespanning_l1'
    elif obis == '1-0:52.36.0':
        return 'aantaltehogespanning_l2'
    elif obis == '1-0:72.36.0':
        return 'aantaltehogespanning_l3'
    elif obis == '0-0:96.13.0':
        return 'text_message'
    elif obis == '1-0:32.7.0':
        return 'instantaneousvoltage_l1'
    elif obis == '1-0:52.7.0':
        return 'instantaneousvoltage_l2'
    elif obis == '1-0:72.7.0':
        return 'instantaneousvoltage_l3'
    elif obis == '1-0:31.7.0':
        return 'instantaneouscurrent_l1'
    elif obis == '1-0:51.7.0':
        return 'instantaneouscurrent_l2'
    elif obis == '1-0:71.7.0':
        return 'instantaneouscurrent_l3'
    elif obis == '1-0:21.7.0':
        return 'instantaneouspower_consumed_l1'
    elif obis == '1-0:41.7.0':
        return 'instantaneouspower_consumed_l2'
    elif obis == '1-0:61.7.0':
        return 'instantaneouspower_consumed_l3'
    elif obis == '1-0:22.7.0':
        return 'instantaneouspower_produced_l1'
    elif obis == '1-0:42.7.0':
        return 'instantaneouspower_produced_l2'
    elif obis == '1-0:62.7.0':
        return 'instantaneouspower_produced_l3'
    return 'error'


def electra_value(value, unit):
    electraparser = re.compile(r'(\d+\.?\d+)\*'+unit)
    parsed = electraparser.match(value)
    if parsed:
        return float(parsed.group(1))
    else:
        return None


class PowerFailureEvent:
    def __init__(self, endtime, duration):
        endtime = endtime[:-1]
        self._timestamp_end = datetime.datetime.strptime(endtime, "%y%m%d%H%M%S")
        duration_parser = re.compile(r'(\d+)\*s')
        duration_parser.match(duration)
        self._duration_in_sec = int(duration_parser.match(duration).group(1))

    @property
    def timestamp_end(self):
        return self._timestamp_end

    @property
    def duration(self):
        return self._duration_in_sec, "s"

    def __str__(self):
        return str(self._timestamp_end.strftime("%Y-%m-%d %H:%M:%S")) + " " + str(self._duration_in_sec) + " secondes"


class MbusDevice:
    def __init__(self):
        self._id = -1
        self._devicetype = -1
        self._timestamp = datetime.datetime.now()
        self._measurement = 0.0
        self._unit = ""
        self._error = ""

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = int(value[0])

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def devicetype(self):
        return self._devicetype

    @devicetype.setter
    def devicetype(self, value):
        self._devicetype = int(value[0])

    @property
    def measurement(self):
        return self._measurement

    @measurement.setter
    def measurement(self, value):
        timestamp = value[0]
        timestamp = timestamp[:-1]
        self._timestamp = datetime.datetime.strptime(timestamp, "%y%m%d%H%M%S")
        parser = re.compile(r'(\d+\.?\d+)\*(.+)')
        meteringvalue = parser.match(value[1])
        if meteringvalue:
            self._measurement = float(meteringvalue.group(1))
            self._unit = meteringvalue.group(2)
        else:
            self.error = "Could not parse measurement for device: " + str(self._devicetype) + " value: " + str(value)

    @property
    def unit(self):
        return self._unit

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        if self.error == "":
            self._error = str(value)
        else:
            self._error = self._error + "\n" + str(value)

    def __str__(self):
        return str(self._timestamp.strftime("%Y-%m-%d %H:%M:%S")) + " " + str(self.measurement) + " " + self._unit


class TelegramEntityException(Exception):
    def __init__(self, message):
        super(TelegramEntityException, self).__init__(message)


class Telegram:
    def __init__(self):
        self._manufacture = ""
        self._version = -1
        self._timestamp = datetime.datetime.now()
        self._error = ""
        self._meter_id = -1
        self._meterstandelectra_consumed_tariff1 = -1
        self._meterstandelectra_consumed_tariff2 = -1
        self._meterstandelectra_produced_tariff1 = -1
        self._meterstandelectra_produced_tariff2 = -1
        self._actualtariff = -1
        self._actualpower_consumed = -1
        self._actualpower_produced = -1
        self._aantalstoringen = -1
        self._aantallangdurigestoringen = -1
        self._power_failure_events = []
        self._aantaltelagespanning_l1 = -1
        self._aantaltelagespanning_l2 = -1
        self._aantaltelagespanning_l3 = -1
        self._aantaltehogespanning_l1 = -1
        self._aantaltehogespanning_l2 = -1
        self._aantaltehogespanning_l3 = -1
        self._instantaneousvoltage_l1 = -1
        self._instantaneousvoltage_l2 = -1
        self._instantaneousvoltage_l3 = -1
        self._instantaneouscurrent_l1 = -1
        self._instantaneouscurrent_l2 = -1
        self._instantaneouscurrent_l3 = -1
        self._instantaneouspower_consumed_l1 = -1
        self._instantaneouspower_consumed_l2 = -1
        self._instantaneouspower_consumed_l3 = -1
        self._instantaneouspower_produced_l1 = -1
        self._instantaneouspower_produced_l2 = -1
        self._instantaneouspower_produced_l3 = -1
        self._text_message = ""
        self._data = {}
        self._mbusdevice = {}

    def is_data_ok(self):
        if self.error == "":
            return True
        return False

    def add(self, line):
        if self._manufacture:
            lineparser = re.compile(r'(\d+?-\d+?:\d+?\.\d+?\.\d+?)(\(.*\))')
            mbus_pattern = re.compile(r'0-([1234]):((24|96)\.[12]\.[01])')
            parsed = lineparser.match(line)
            if parsed:
                obis_reference = parsed.group(1)
                mbus_match = mbus_pattern.match(obis_reference)
                valueparser = re.compile(r'\((.*?)\)')
                measurements = valueparser.findall(parsed.group(2))
                if measurements:
                    if mbus_match:
                        channel_id = mbus_match.group(1)
                        self.set_mbusdevice(channel_id, mbus_match.group(2), measurements)
                    else:
                        try:
                            setattr(self, obis2attribute(obis_reference), measurements)
                        except AttributeError:
                            self.error = "Can't set attribute for: " + obis_reference
                        if self._error:
                            print(obis_reference + " : " + str(measurements))
                            raise TelegramEntityException(self.error)
                else:
                    print("MAG NIET: " + line)
        else:
            if '\\' in line:
                self._manufacture = line
            else:
                raise TelegramEntityException("Wrong format of manufacture line: " + str(line))

    def set_mbusdevice(self, channel_id, obis_subreference, value):
        if channel_id not in self._mbusdevice:
            self._mbusdevice[channel_id] = MbusDevice()
        if obis_subreference == '24.1.0':
            self._mbusdevice[channel_id].devicetype = value
        elif obis_subreference == '96.1.0':
            self._mbusdevice[channel_id].id = value
        elif obis_subreference == '24.2.1':
            self._mbusdevice[channel_id].measurement = value
        else:
            self.error = "Wrong mbusdevice reference value: " + str(channel_id) + str(obis_subreference) + str(value)
        if self._mbusdevice[channel_id].error != "":
            self.error = self._mbusdevice[channel_id].error

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        if self.error == "":
            self._error = str(value)
        else:
            self._error = self._error + "\n" + str(value)

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = int(value[0])

    @property
    def manufacture(self):
        return self._manufacture

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        # YYMMDDhhmm ssX
        timestamp = value[0][:-1]
        try:
            self._timestamp = datetime.datetime.strptime(timestamp, "%y%m%d%H%M%S")
        except ValueError:
            self._error = "Not a valid timestamp: " + timestamp

    @property
    def meter_id(self):
        return self._meter_id

    @meter_id.setter
    def meter_id(self, value):
        self._meter_id = int(value[0])

    @property
    def meterstandelectra_consumed_tariff1(self):
        return self._meterstandelectra_consumed_tariff1, "kWh"

    @meterstandelectra_consumed_tariff1.setter
    def meterstandelectra_consumed_tariff1(self, value):
        electra = electra_value(value[0], "kWh")
        if electra is not None:
            self._meterstandelectra_consumed_tariff1 = electra
        else:
            self.error = "meterstandelectra_consumed_tariff1 parsing failed: " + str(value)

    @property
    def meterstandelectra_consumed_tariff2(self):
        return self._meterstandelectra_consumed_tariff2, "kWh"

    @meterstandelectra_consumed_tariff2.setter
    def meterstandelectra_consumed_tariff2(self, value):
        electra = electra_value(value[0], "kWh")
        if electra is not None:
            self._meterstandelectra_consumed_tariff2 = electra
        else:
            self.error = "meterstandelectra_consumed_tariff2 parsing failed: " + str(value)

    @property
    def meterstandelectra_produced_tariff1(self):
        return self._meterstandelectra_produced_tariff1, "kWh"

    @meterstandelectra_produced_tariff1.setter
    def meterstandelectra_produced_tariff1(self, value):
        electra = electra_value(value[0], "kWh")
        if electra is not None:
            self._meterstandelectra_produced_tariff1 = electra
        else:
            self.error = "meterstandelectra_produced_tariff1 parsing failed: " + str(value)

    @property
    def meterstandelectra_produced_tariff2(self):
        return self._meterstandelectra_produced_tariff2, "kWh"

    @meterstandelectra_produced_tariff2.setter
    def meterstandelectra_produced_tariff2(self, value):
        electra = electra_value(value[0], "kWh")
        if electra is not None:
            self._meterstandelectra_produced_tariff2 = electra
        else:
            self.error = "meterstandelectra_produced_tariff2 parsing failed: " + str(value)

    @property
    def actualtariff(self):
        if self._actualtariff == 1:
            return "low"
        elif self._actualtariff == 2:
            return "high"

    @actualtariff.setter
    def actualtariff(self, value):
        tariff_code = int(value[0])
        if tariff_code in [0, 1]:
            self._actualtariff = tariff_code
        else:
            self.error = "tariff code wrong: " + value[0]

    @property
    def actualpower_consumed(self):
        return self._actualpower_consumed, "kW"

    @actualpower_consumed.setter
    def actualpower_consumed(self, value):
        electra = electra_value(value[0], "kW")
        if electra is not None:
            self._actualpower_consumed = electra
        else:
            self.error = "Parsing failed actualpower_consumed: " + str(value)

    @property
    def actualpower_produced(self):
        return self._actualpower_produced, "kW"

    @actualpower_produced.setter
    def actualpower_produced(self, value):
        electra = electra_value(value[0], "kW")
        if electra is not None:
            self._actualpower_produced = electra
        else:
            self.error = "Parsing failed actualpower_produced: " + str(value)

    @property
    def aantalstoringen(self):
        return self._aantalstoringen

    @aantalstoringen.setter
    def aantalstoringen(self, value):
        self._aantalstoringen = int(value[0])

    @property
    def aantallangdurigestoringen(self):
        return self._aantallangdurigestoringen

    @aantallangdurigestoringen.setter
    def aantallangdurigestoringen(self, value):
        self._aantallangdurigestoringen = int(value[0])

    @property
    def power_failure_events(self):
        return self._power_failure_events

    @power_failure_events.setter
    def power_failure_events(self, value):
        nr_of_events = int(value[0])
        for event in range(1, nr_of_events + 1):
            powerfailure = PowerFailureEvent(value[event*2], value[(event * 2) + 1])
            self._power_failure_events.append(powerfailure)

    @property
    def aantaltelagespanning_l1(self):
        return self._aantaltelagespanning_l1

    @aantaltelagespanning_l1.setter
    def aantaltelagespanning_l1(self, value):
        self._aantaltelagespanning_l1 = int(value[0])

    @property
    def aantaltelagespanning_l2(self):
        return self._aantaltelagespanning_l2

    @aantaltelagespanning_l2.setter
    def aantaltelagespanning_l2(self, value):
        self._aantaltelagespanning_l2 = int(value[0])

    @property
    def aantaltelagespanning_l3(self):
        return self._aantaltelagespanning_l3

    @aantaltelagespanning_l3.setter
    def aantaltelagespanning_l3(self, value):
        self._aantaltelagespanning_l3 = int(value[0])

    @property
    def aantaltehogespanning_l1(self):
        return self._aantaltehogespanning_l1

    @aantaltehogespanning_l1.setter
    def aantaltehogespanning_l1(self, value):
        self._aantaltehogespanning_l1 = int(value[0])

    @property
    def aantaltehogespanning_l2(self):
        return self._aantaltehogespanning_l2

    @aantaltehogespanning_l2.setter
    def aantaltehogespanning_l2(self, value):
        self._aantaltehogespanning_l2 = int(value[0])

    @property
    def aantaltehogespanning_l3(self):
        return self._aantaltehogespanning_l3

    @aantaltehogespanning_l3.setter
    def aantaltehogespanning_l3(self, value):
        self._aantaltehogespanning_l3 = int(value[0])

    @property
    def text_message(self):
        return self._text_message

    @text_message.setter
    def text_message(self, value):
        self._text_message = value[0]

    @property
    def instantaneousvoltage_l1(self):
        return self._instantaneousvoltage_l1, "V"

    @instantaneousvoltage_l1.setter
    def instantaneousvoltage_l1(self, value):
        electra = electra_value(value[0], "V")
        if electra is not None:
            self._instantaneousvoltage_l1 = electra
        else:
            self.error = "Parsing failed voltage_l1: " + str(value)

    @property
    def instantaneousvoltage_l2(self):
        return self._instantaneousvoltage_l2, "V"

    @instantaneousvoltage_l2.setter
    def instantaneousvoltage_l2(self, value):
        electra = electra_value(value[0], "V")
        if electra is not None:
            self._instantaneousvoltage_l2 = electra
        else:
            self.error = "Parsing failed voltage_l2: " + str(value)

    @property
    def instantaneousvoltage_l3(self):
        return self._instantaneousvoltage_l3, "V"

    @instantaneousvoltage_l3.setter
    def instantaneousvoltage_l3(self, value):
        electra = electra_value(value[0], "V")
        if electra is not None:
            self._instantaneousvoltage_l3 = electra
        else:
            self.error = "Parsing failed voltage_l3: " + str(value)

    @property
    def instantaneouscurrent_l1(self):
        return self._instantaneouscurrent_l1, "A"

    @instantaneouscurrent_l1.setter
    def instantaneouscurrent_l1(self, value):
        electra = electra_value(value[0], "A")
        if electra is not None:
            self._instantaneouscurrent_l1 = int(electra)
        else:
            self.error = "Parsing failed instantaneouscurrent_l1: " + str(value)

    @property
    def instantaneouscurrent_l2(self):
        return self._instantaneouscurrent_l2, "A"

    @instantaneouscurrent_l2.setter
    def instantaneouscurrent_l2(self, value):
        electra = electra_value(value[0], "A")
        if electra is not None:
            self._instantaneouscurrent_l2 = int(electra)
        else:
            self.error = "Parsing failed instantaneouscurrent_l2: " + str(value)

    @property
    def instantaneouscurrent_l3(self):
        return self._instantaneouscurrent_l3, "A"

    @instantaneouscurrent_l3.setter
    def instantaneouscurrent_l3(self, value):
        electra = electra_value(value[0], "A")
        if electra is not None:
            self._instantaneouscurrent_l3 = int(electra)
        else:
            self.error = "Parsing failed instantaneouscurrent_l3: " + str(value)

    @property
    def instantaneouspower_consumed_l1(self):
        return self._instantaneouspower_consumed_l1, "kW"

    @instantaneouspower_consumed_l1.setter
    def instantaneouspower_consumed_l1(self, value):
        electra = electra_value(value[0], "kW")
        if electra is not None:
            self._instantaneouspower_consumed_l1 = electra
        else:
            self.error = "Parsing failed instantaneouspower_consumed_l1: " + str(value)

    @property
    def instantaneouspower_consumed_l2(self):
        return self._instantaneouspower_consumed_l2, "kW"

    @instantaneouspower_consumed_l2.setter
    def instantaneouspower_consumed_l2(self, value):
        electra = electra_value(value[0], "kW")
        if electra is not None:
            self._instantaneouspower_consumed_l2 = electra
        else:
            self.error = "Parsing failed instantaneouspower_consumed_l2: " + str(value)

    @property
    def instantaneouspower_consumed_l3(self):
        return self._instantaneouspower_consumed_l3, "kW"

    @instantaneouspower_consumed_l3.setter
    def instantaneouspower_consumed_l3(self, value):
        electra = electra_value(value[0], "kW")
        if electra is not None:
            self._instantaneouspower_consumed_l3 = electra
        else:
            self.error = "Parsing failed instantaneouspower_consumed_l3: " + str(value)

    @property
    def instantaneouspower_produced_l1(self):
        return self._instantaneouspower_produced_l1, "kW"

    @instantaneouspower_produced_l1.setter
    def instantaneouspower_produced_l1(self, value):
        electra = electra_value(value[0], "kW")
        if electra is not None:
            self._instantaneouspower_produced_l1 = electra
        else:
            self.error = "Parsing failed instantaneouspower_produced_l1: " + str(value)

    @property
    def instantaneouspower_produced_l2(self):
        return self._instantaneouspower_produced_l2, "kW"

    @instantaneouspower_produced_l2.setter
    def instantaneouspower_produced_l2(self, value):
        electra = electra_value(value[0], "kW")
        if electra is not None:
            self._instantaneouspower_produced_l2 = electra
        else:
            self.error = "Parsing failed instantaneouspower_produced_l2: " + str(value)

    @property
    def instantaneouspower_produced_l3(self):
        return self._instantaneouspower_produced_l3, "kW"

    @instantaneouspower_produced_l3.setter
    def instantaneouspower_produced_l3(self, value):
        electra = electra_value(value[0], "kW")
        if electra is not None:
            self._instantaneouspower_produced_l3 = electra
        else:
            self.error = "Parsing failed instantaneouspower_produced_l3: " + str(value)

    @property
    def gasmeter(self):
        for device in self._mbusdevice.values():
            if device.devicetype == 3:
                return device.timestamp, device.id, device.measurement,  device.unit
        return None

    def get_properties(self):
        props = []
        for prop in self.__dir__():
            if not prop.startswith('_'):
                if not inspect.ismethod(getattr(self, prop)):
                    props.append((prop, self.__getattribute__(prop)))
        return props

import re
import datetime


def obis2attribute(obis):
    if obis == '1-3:0.2.8':
        return 'version'
    elif obis == '0-0:1.0.0':
        return 'timestamp'
    elif obis == '0-0:96.1.1':
        return 'meter_id'
    elif obis == '1-0:1.8.1':
        return 'electra_consumed_tariff_1'
    elif obis == '1-0:1.8.2':
        return 'electra_consumed_tariff_2'
    elif obis == '1-0:2.8.1':
        return 'electra_produced_tariff_1'
    elif obis == '1-0:2.8.2':
        return 'electra_produced_tariff_2'
    elif obis == '0-0:96.14.0':
        return 'current_tariff'
    elif obis == '1-0:1.7.0':
        return 'current_electra_consumed'
    elif obis == '1-0:2.7.0':
        return 'current_electra_produced'
    elif obis == '0-0:96.7.21':
        return 'nr_of_power_failures_any_phase'
    elif obis == '0-0:96.7.9':
        return 'nr_of_long_power_failures_any_phase'
    elif obis == '1-0:99.97.0':
        return 'power_failure_events'
    elif obis == '1-0:32.32.0':
        return 'nr_of_voltage_sags_l1'
    elif obis == '1-0:52.32.0':
        return 'nr_of_voltage_sags_l2'
    elif obis == '1-0:72.32.0':
        return 'nr_of_voltage_sags_l3'
    elif obis == '1-0:32.36.0':
        return 'nr_of_voltage_swells_l1'
    elif obis == '1-0:52.36.0':
        return 'nr_of_voltage_swells_l2'
    elif obis == '1-0:72.36.0':
        return 'nr_of_voltage_swells_l3'
    elif obis == '0-0:96.13.0':
        return 'text_message'
    elif obis == '1-0:32.7.0':
        return 'voltage_l1'
    elif obis == '1-0:52.7.0':
        return 'voltage_l2'
    elif obis == '1-0:72.7.0':
        return 'voltage_l3'
    elif obis == '1-0:31.7.0':
        return 'current_l1'
    elif obis == '1-0:51.7.0':
        return 'current_l2'
    elif obis == '1-0:71.7.0':
        return 'current_l3'
    elif obis == '1-0:21.7.0':
        return 'power_consumed_l1'
    elif obis == '1-0:41.7.0':
        return 'power_consumed_l2'
    elif obis == '1-0:61.7.0':
        return 'power_consumed_l3'
    elif obis == '1-0:22.7.0':
        return 'power_produced_l1'
    elif obis == '1-0:42.7.0':
        return 'power_produced_l2'
    elif obis == '1-0:62.7.0':
        return 'power_produced_l3'
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

    def __str__(self):
        return str(self._timestamp_end.strftime("%Y-%m-%d %H:%M:%S")) + " " + str(self._duration_in_sec) + " secondes"


class MbusDevice:
    def __init__(self):
        print("MbusDevice")
        self._id = -1
        self._devicetype = -1
        self._timestamp = datetime.datetime.now()
        self._measurement = 0.0
        self._unit = ""

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = int(value[0])
        print("\tId: " + str(self.id))

    @property
    def devicetype(self):
        return self._devicetype

    @devicetype.setter
    def devicetype(self, value):
        self._devicetype = int(value[0])
        print("\tType: " + str(self.devicetype))

    @property
    def measurement(self):
        return self._measurement

    @measurement.setter
    def measurement(self, value):
        timestamp = value[0]
        timestamp = timestamp[:-1]
        self._timestamp = datetime.datetime.strptime(timestamp, "%y%m%d%H%M%S")
        parser = re.compile(r'(\d+\.?\d+)\*(.+?)')
        meteringvalue = parser.match(value[1])
        if meteringvalue:
            self._measurement = float(meteringvalue.group(1))
            self._unit = meteringvalue.group(2)
            print("\tmeasurement: " + str(self))

    def __str__(self):
        return str(self._timestamp.strftime("%Y-%m-%d %H:%M:%S")) + " " + str(self.measurement) + " " + self._unit


class Telegram:
    def __init__(self):
        self._manufacture = ""
        self._version = -1
        self._timestamp = datetime.datetime.now()
        self._error = ""
        self._meter_id = -1
        self._electra_consumed_tariff_1 = -1
        self._electra_consumed_tariff_2 = -1
        self._electra_produced_tariff_1 = -1
        self._electra_produced_tariff_2 = -1
        self._current_tariff = -1
        self._current_electra_consumed = -1
        self._current_electra_produced = -1
        self._nr_of_power_failures_any_phase = -1
        self._nr_of_long_power_failures_any_phase = -1
        self._power_failure_events = []
        self._nr_of_voltage_sags_l1 = -1
        self._nr_of_voltage_sags_l2 = -1
        self._nr_of_voltage_sags_l3 = -1
        self._nr_of_voltage_swells_l1 = -1
        self._nr_of_voltage_swells_l2 = -1
        self._nr_of_voltage_swells_l3 = -1
        self._voltage_l1 = -1
        self._voltage_l2 = -1
        self._voltage_l3 = -1
        self._current_l1 = -1
        self._current_l2 = -1
        self._current_l3 = -1
        self._power_consumed_l1 = -1
        self._power_consumed_l2 = -1
        self._power_consumed_l3 = -1
        self._power_produced_l1 = -1
        self._power_produced_l2 = -1
        self._power_produced_l3 = -1
        self._text_message = ""
        self._data = {}
        self._mbusdevice = {}

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
                        setattr(self, obis2attribute(obis_reference), measurements)
                        if self._error:
                            print("Error: " + str(self._error))
                            print(obis_reference + " : " + str(measurements))
                else:
                    print("MAG NIET: " + line)
        else:
            self._manufacture = line

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
            print("error: wrong mbusdevice reference value: " + str(channel_id) + str(obis_subreference) + str(value))

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = int(value[0])
        print("Version: " + str(self.version))

    @property
    def timestamp(self):
        return self._timestamp.strftime("%Y-%m-%d %H:%M:%S")

    @timestamp.setter
    def timestamp(self, value):
        # YYMMDDhhmm ssX
        timestamp = value[0][:-1]
        try:
            self._timestamp = datetime.datetime.strptime(timestamp, "%y%m%d%H%M%S")
            print("datimetime: " + self.timestamp)
        except:
            self._error = "Not a valid timestamp: " + timestamp

    @property
    def meter_id(self):
        return self._meter_id

    @meter_id.setter
    def meter_id(self, value):
        self._meter_id = int(value[0])
        print("Meter ID: " + str(self.meter_id))

    @property
    def electra_consumed_tariff_1(self):
        return self._electra_consumed_tariff_1

    @electra_consumed_tariff_1.setter
    def electra_consumed_tariff_1(self, value):
        electra = electra_value(value[0], "kWh")
        if electra is not None:
            self._electra_consumed_tariff_1 = electra
            print("Electra consumed 1: " + str(self.electra_consumed_tariff_1) + " kWh")
        else:
            print("electra_consumed_tariff_1 parsing failed: " + str(value))

    @property
    def electra_consumed_tariff_2(self):
        return self._electra_consumed_tariff_2

    @electra_consumed_tariff_2.setter
    def electra_consumed_tariff_2(self, value):
        electra = electra_value(value[0], "kWh")
        if electra is not None:
            self._electra_consumed_tariff_2 = electra
            print("Electra consumed 2: " + str(self.electra_consumed_tariff_2) + " kWh")
        else:
            print("electra_consumed_tariff_2 parsing failed: " + str(value))

    @property
    def electra_produced_tariff_1(self):
        return self._electra_produced_tariff_1

    @electra_produced_tariff_1.setter
    def electra_produced_tariff_1(self, value):
        electra = electra_value(value[0], "kWh")
        if electra is not None:
            self._electra_produced_tariff_1 = electra
            print("Electra produced 1: " + str(self.electra_produced_tariff_1) + " kWh")
        else:
            print("electra_produced_tariff_1 parsing failed: " + str(value))

    @property
    def electra_produced_tariff_2(self):
        return self._electra_produced_tariff_2

    @electra_produced_tariff_2.setter
    def electra_produced_tariff_2(self, value):
        electra = electra_value(value[0], "kWh")
        if electra is not None:
            self._electra_produced_tariff_2 = electra
            print("Electra produced 2: " + str(self.electra_produced_tariff_2) + " kWh")
        else:
            print("electra_produced_tariff_2 parsing failed: " + str(value))

    @property
    def current_tariff(self):
        return self._current_tariff

    @current_tariff.setter
    def current_tariff(self, value):
        tariff_code = int(value[0])
        if tariff_code in [0, 1]:
            self._current_tariff = tariff_code
            print("Current Tariff: " + str(self.current_tariff))
        else:
            print("tariff code wrong: " + value[0])

    @property
    def current_electra_consumed(self):
        return self._current_electra_consumed

    @current_electra_consumed.setter
    def current_electra_consumed(self, value):
        electra = electra_value(value[0], "kW")
        if electra is not None:
            self._current_electra_consumed = electra
            print("Current electra consumed: " + str(self.current_electra_consumed) + " kW")
        else:
            print("Parsing failed current_electra_consumed: " + str(value))

    @property
    def current_electra_produced(self):
        return self._current_electra_produced

    @current_electra_produced.setter
    def current_electra_produced(self, value):
        electra = electra_value(value[0], "kW")
        if electra is not None:
            self._current_electra_produced = electra
            print("Current electra produced: " + str(self.current_electra_produced) + " kW")
        else:
            print("Parsing failed current_electra_produced: " + str(value))

    @property
    def nr_of_power_failures_any_phase(self):
        return self._nr_of_power_failures_any_phase

    @nr_of_power_failures_any_phase.setter
    def nr_of_power_failures_any_phase(self, value):
        self._nr_of_power_failures_any_phase = int(value[0])
        print("Number of power failures in any phase: " + str(self._nr_of_power_failures_any_phase))

    @property
    def nr_of_long_power_failures_any_phase(self):
        return self._nr_of_long_power_failures_any_phase

    @nr_of_long_power_failures_any_phase.setter
    def nr_of_long_power_failures_any_phase(self, value):
        self._nr_of_long_power_failures_any_phase = int(value[0])
        print("Number of long power failures in any phase: " + str(self._nr_of_long_power_failures_any_phase))

    @property
    def power_failure_events(self):
        return self._power_failure_events

    @power_failure_events.setter
    def power_failure_events(self, value):
        nr_of_events = int(value[0])
        for event in range(1, nr_of_events + 1):
            powerfailure = PowerFailureEvent(value[event*2], value[(event * 2) +1])
            self._power_failure_events.append(powerfailure)
        for event in self._power_failure_events:
            print("\tPower failure event: " + str(event))

    @property
    def nr_of_voltage_sags_l1(self):
        return self._nr_of_voltage_sags_l1

    @nr_of_voltage_sags_l1.setter
    def nr_of_voltage_sags_l1(self, value):
        self._nr_of_voltage_sags_l1 = int(value[0])
        print("Number of Voltage dips l1: " + str(self.nr_of_voltage_sags_l1))

    @property
    def nr_of_voltage_sags_l2(self):
        return self._nr_of_voltage_sags_l2

    @nr_of_voltage_sags_l2.setter
    def nr_of_voltage_sags_l2(self, value):
        self._nr_of_voltage_sags_l2 = int(value[0])
        print("Number of Voltage dips l2: " + str(self.nr_of_voltage_sags_l2))

    @property
    def nr_of_voltage_sags_l3(self):
        return self._nr_of_voltage_sags_l3

    @nr_of_voltage_sags_l3.setter
    def nr_of_voltage_sags_l3(self, value):
        self._nr_of_voltage_sags_l3 = int(value[0])
        print("Number of Voltage dips l3: " + str(self.nr_of_voltage_sags_l3))

    @property
    def nr_of_voltage_swells_l1(self):
        return self._nr_of_voltage_swells_l1

    @nr_of_voltage_swells_l1.setter
    def nr_of_voltage_swells_l1(self, value):
        self._nr_of_voltage_swells_l1 = int(value[0])
        print("Number of Voltage swells l1: " + str(self.nr_of_voltage_swells_l1))

    @property
    def nr_of_voltage_swells_l2(self):
        return self._nr_of_voltage_swells_l2

    @nr_of_voltage_swells_l2.setter
    def nr_of_voltage_swells_l2(self, value):
        self._nr_of_voltage_swells_l2 = int(value[0])
        print("Number of Voltage swells l2: " + str(self.nr_of_voltage_swells_l2))

    @property
    def nr_of_voltage_swells_l3(self):
        return self._nr_of_voltage_swells_l3

    @nr_of_voltage_swells_l3.setter
    def nr_of_voltage_swells_l3(self, value):
        self._nr_of_voltage_swells_l3 = int(value[0])
        print("Number of Voltage swells l3: " + str(self.nr_of_voltage_swells_l3))

    @property
    def text_message(self):
        return self._text_message

    @text_message.setter
    def text_message(self, value):
        self._text_message = value[0]
        print("Text Message: " + self.text_message)

    @property
    def voltage_l1(self):
        return self._voltage_l1

    @voltage_l1.setter
    def voltage_l1(self, value):
        electra = electra_value(value[0], "V")
        if electra is not None:
            self._voltage_l1 = electra
            print("Voltage L1: " + str(self.voltage_l1) + " V")
        else:
            print("Parsing failed voltage_l1: " + str(value))

    @property
    def voltage_l2(self):
        return self._voltage_l2

    @voltage_l2.setter
    def voltage_l2(self, value):
        electra = electra_value(value[0], "V")
        if electra is not None:
            self._voltage_l2 = electra
            print("Voltage L2: " + str(self.voltage_l2) + " V")
        else:
            print("Parsing failed voltage_l2: " + str(value))

    @property
    def voltage_l3(self):
        return self._voltage_l3

    @voltage_l3.setter
    def voltage_l3(self, value):
        electra = electra_value(value[0], "V")
        if electra is not None:
            self._voltage_l3 = electra
            print("Voltage L3: " + str(self.voltage_l3) + " V")
        else:
            print("Parsing failed voltage_l3: " + str(value))

    @property
    def current_l1(self):
        return self._current_l1

    @current_l1.setter
    def current_l1(self, value):
        electra = electra_value(value[0], "A")
        if electra is not None:
            self._current_l1 = int(electra)
            print("Current L1: " + str(self.current_l1) + " A")
        else:
            print("Parsing failed current_l1: " + str(value))

    @property
    def current_l2(self):
        return self._current_l2

    @current_l2.setter
    def current_l2(self, value):
        electra = electra_value(value[0], "A")
        if electra is not None:
            self._current_l2 = int(electra)
            print("Current L2: " + str(self.current_l2) + " A")
        else:
            print("Parsing failed current_l2: " + str(value))

    @property
    def current_l3(self):
        return self._current_l3

    @current_l3.setter
    def current_l3(self, value):
        electra = electra_value(value[0], "A")
        if electra is not None:
            self._current_l3 = int(electra)
            print("Current L3: " + str(self.current_l3) + " A")
        else:
            print("Parsing failed current_l3: " + str(value))

    @property
    def power_consumed_l1(self):
        return self._power_consumed_l1

    @power_consumed_l1.setter
    def power_consumed_l1(self, value):
        electra = electra_value(value[0], "kW")
        if electra is not None:
            self._power_consumed_l1 = electra
            print("Power consumed L1: " + str(self.power_consumed_l1) + " kW")

    @property
    def power_consumed_l2(self):
        return self._power_consumed_l2

    @power_consumed_l2.setter
    def power_consumed_l2(self, value):
        electra = electra_value(value[0], "kW")
        if electra is not None:
            self._power_consumed_l2 = electra
            print("Power consumed L2: " + str(self.power_consumed_l2) + " kW")

    @property
    def power_consumed_l3(self):
        return self._power_consumed_l3

    @power_consumed_l3.setter
    def power_consumed_l3(self, value):
        electra = electra_value(value[0], "kW")
        if electra is not None:
            self._power_consumed_l3 = electra
            print("Power consumed L3: " + str(self.power_consumed_l3) + " kW")

    @property
    def gas_meter(self):
        for device in self._mbusdevice.values():
            if device.devicetype == 3:
                return device
        return None

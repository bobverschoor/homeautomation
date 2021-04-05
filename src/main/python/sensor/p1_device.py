from smeterd.meter import SmartMeter
import json


class P1Device:
    E_LAAG = 'low'
    E_HOOG = 'high'
    E_CONSUMED = 'consumed'
    E_PRODUCED = 'produced'
    G_M3 = 'm3'
    G_TIMESTAMP = 'timestamp'

    def __init__(self, file='/dev/ttyUSB0'):
        self.meter = SmartMeter(file, baudrate=115200, parity='N', stopbits=1, bytesize=8)

    def get_data(self):
        with self.meter:
            packet = self.meter.read_one_packet()
        e = {}
        metername = str(packet['header'])[:1]

        for tarief in [P1Device.E_LAAG, P1Device.E_HOOG]:
            e[tarief] = {}
            for richting in [P1Device.E_CONSUMED, P1Device.E_PRODUCED]:
                e[tarief][richting] = packet['kwh'][tarief][richting]
        g = {P1Device.G_M3: packet['gas']['total'], P1Device.G_TIMESTAMP: packet['gas']['measured_at']}
        data = {"electra": e, 'gas': g, 'header':packet['header']}
        return str(json.dumps(data))

# {"electra": {"low": {"consumed": 16351.117, "produced": 1.804}, "high": {"consumed": 20121.471, "produced": 0.007}}, "gas": {"m3": 7368.67, "timestamp": 1601391600}}

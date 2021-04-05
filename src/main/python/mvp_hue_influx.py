from sensor.home_gateway import HomeGateway
from sensor.hue_bridge_device import HueBridgeDevice

homegateway = HomeGateway()
homegateway.add_device(HueBridgeDevice())


for switch in homegateway.get_switches():
    print(switch)

for lights in homegateway.get_lights():
    print(lights)
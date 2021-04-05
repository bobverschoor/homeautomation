class HomeGateway:

    def __init__(self):
        self.devices = set()

    def add_device(self, home_device):
        self.devices.add(home_device)

    def get_switches(self):
        switches = []
        for device in self.devices:
            for entity in device.get_entities():
                switches.append(entity)
        return switches

    def get_lights(self):
        lights = []
        for device in self.devices:
            lights.append(device)
        return lights





class MockGpio:
    PUD_DOWN = 1
    BOARD = 1
    IN = 1
    OUT = 2
    HIGH = 1
    LOW = 0

    def __init__(self):
        self.IN = ""
        self.OUT = ""
        self.input_waarde = -1
        self.pin = {}

    def setup(self, pin, io, pull_up_down="PUD_DOWN"):
        self.pin[pin] = -1

    def input(self, input):
        return self.input_waarde

    def output(self, pin, waarde):
        self.pin[pin] = waarde
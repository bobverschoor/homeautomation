# Puur voor ontwikkel doeleinden. Deze wordt conditional imported

PUD_DOWN = 1
BOARD = 1
IN = 1
OUT = 2
HIGH = 1
LOW = 0

print("WARN: Using DEV version of GPIO. If unintential, install GPIO library first!")


def setwarnings(value):
    print("Mock GPIO.PY")


def setmode(value):
    print("Mock GPIO.PY")


def setup(pin, io, pull_up_down=PUD_DOWN):
    print("Mock GPIO.PY")


def input(pin):
    print("Mock GPIO.PY")
    return pin


def output(pin, waarde):
    print("Mock GPIO.PY")


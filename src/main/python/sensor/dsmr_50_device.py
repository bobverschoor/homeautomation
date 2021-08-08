import serial

from entiteiten.telegram import Telegram


class DSMR_50:
    def __init__(self):
        self.serial = serial.Serial()
        self.serial.baudrate = 115200
        self.serial.bytesize = serial.EIGHTBITS
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.xonxoff = 0
        self.serial.rtscts = 0
        self.serial.timeout = 20
        self.serial.port = "/dev/ttyUSB0"

    def read_telegram(self):
        telegram = Telegram()
        with self.serial as ser:
            while True:
                p1_raw_line = ser.readline()
                if lastline(p1_raw_line):
                    break
                p1_line = str(p1_raw_line.strip(b'\r\n '), 'UTF-8')
                if p1_line != b'\x00' and len(p1_line) > 1:
                    telegram.add(p1_line)
        return telegram


def lastline(line):
    if len(line) > 0:
        if line[0] == 33:  # starts with ! Einde telegram eindigt altijd met ! en getal
            return True
    return False

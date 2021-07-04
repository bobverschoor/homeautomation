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
                if p1_line != b'\x00' and p1_line != "":
                    telegram.add(p1_line)
        return telegram


def lastline(line):
    if len(line) > 0:
        if line[0] == 33:  # starts with ! Einde telegram eindigt altijd met ! en getal
            return True
    return False
#
# #Initialize
# # stack is mijn list met de 26 regeltjes.
# p1_teller=0
# stack=[]
#
# while p1_teller < 26:
#     p1_line=''
#     #Read 1 line
#     try:
#         p1_raw = ser.readline()
#     except:
#         sys.exit ("Seriele poort %s kan niet gelezen worden. Programma afgebroken." % ser.name )
#     p1_str=str(p1_raw)
#     #p1_str=str(p1_raw, "utf-8")
#     p1_line=p1_str.strip()
#     stack.append(p1_line)
#     # als je alles wil zien moet je de volgende line uncommenten
#     #    print (p1_line)
#     p1_teller = p1_teller +1

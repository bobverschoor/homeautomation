import serial

from entiteiten.telegram import Telegram, TelegramEntityException


class SerialBus:
    def __init__(self, serialport):
        self.serial = serial.Serial()
        self.serial.baudrate = 115200
        self.serial.bytesize = serial.EIGHTBITS
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.xonxoff = 0
        self.serial.rtscts = 0
        self.serial.timeout = 20
        self.serial.port = serialport

    def receive_raw_telegram(self):
        raw_telegram_lines = []
        with self.serial as ser:
            while True:
                p1_raw_line = ser.readline()
                if lastline(p1_raw_line):
                    break
                p1_line = str(p1_raw_line.strip(b'\r\n '), 'UTF-8')
                if p1_line != b'\x00' and len(p1_line) > 1:
                    raw_telegram_lines.append(p1_line)
        return raw_telegram_lines


class DSMR_50:
    MIN_LEN_TELEGRAM = 32
    CONFIG_P1METER = 'p1meter'
    CONFIG_SERIALPORT = 'serialport'

    def __init__(self, config):
        if DSMR_50.CONFIG_P1METER in config:
            config = config[DSMR_50.CONFIG_P1METER]
            if DSMR_50.CONFIG_SERIALPORT in config:
                self.serial = SerialBus(config[DSMR_50.CONFIG_SERIALPORT])
            else:
                raise TelegramEntityException(DSMR_50.CONFIG_SERIALPORT + " not in config file")
        else:
            raise TelegramEntityException(DSMR_50.CONFIG_P1METER + " not in config file")

    def read_telegram(self):
        telegram = Telegram()
        raw_telegram = self.serial.receive_raw_telegram()
        if not raw_telegram_ok(raw_telegram):
            # In geval van fout, probeer nog een keer te lezen
            raw_telegram = self.serial.receive_raw_telegram()
        if raw_telegram_ok(raw_telegram):
            for p1_line in raw_telegram:
                try:
                    telegram.add(p1_line)
                except TelegramEntityException as tee:
                    print(tee)
                    print("##### Start Raw Data #####")
                    for line in raw_telegram:
                        print('\t' + str(line))
                    print("##### End   Raw Data #####")
                    print(p1_line)
        return telegram


def lastline(line):
    if len(line) > 0:
        if line[0] == 33:  # starts with ! Einde telegram eindigt altijd met ! en getal
            return True
    return False


def raw_telegram_ok(raw_telegram):
    if len(raw_telegram) > DSMR_50.MIN_LEN_TELEGRAM:
        if raw_telegram[0].startswith('/'):
            return True
    return False

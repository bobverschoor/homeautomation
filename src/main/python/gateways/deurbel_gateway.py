import datetime
import threading
from device.sensor.deurbel_device import DeurbelGong, DeurbelKnop
from entiteiten.meetwaarde import Meetwaarde, convertstr2tags


class DeurbelGatewayException(Exception):
    def __init__(self, message):
        super(DeurbelGatewayException, self).__init__(message)


class DeurbelGateway:
    CONFIG_DEURBEL = 'deurbel'
    CONFIG_GONGDURATION = 'gong_duration_ms'
    CONFIG_GONGDURATION_DEFAULT = 1
    CONFIG_DATABASENAAM = 'databasenaam'

    def __init__(self, config, debug=False):
        self._knop = None
        self._gong = None
        self._ringing = False
        self._debug = debug
        if DeurbelGateway.CONFIG_DEURBEL in config:
            self._config = config[DeurbelGateway.CONFIG_DEURBEL]
            if DeurbelGateway.CONFIG_GONGDURATION in self._config:
                self._gongduration = self._config[DeurbelGateway.CONFIG_GONGDURATION]
            else:
                self._gongduration = DeurbelGateway.CONFIG_GONGDURATION_DEFAULT
        else:
            raise DeurbelGatewayException("Config missing deurbel section")

    def set_deurbel(self):
        self._gong = DeurbelGong(self._config)
        self._knop = DeurbelKnop(self._config)

    def ringing(self):
        self._ringing = True
        self._gong.ring(self._gongduration)
        if self._debug:
            print(str(datetime.datetime.now()) + " Gong heeft geluid.")
        self._ringing = False

    def already_ringing(self):
        return self._ringing

    def knop_ingedrukt(self):
        return self._knop.is_ingedrukt()

    def someone_at_the_deur(self):
        deurbel_gedrukt = False
        if not (self._knop or self._gong):
            self.set_deurbel()
        if self.knop_ingedrukt():
            if self._debug:
                print(str(datetime.datetime.now()) + " Knop is ingedrukt.")
            if self.already_ringing():
                # Returns only once if pressed during ringing
                deurbel_gedrukt = False
            else:
                t = threading.Thread(target=self.ringing)
                t.setDaemon(True)
                t.start()
                deurbel_gedrukt = True
        meetwaarde = Meetwaarde(eenheid='deurbel', tags=convertstr2tags("naam:deurbel"), waarde=deurbel_gedrukt)
        return meetwaarde

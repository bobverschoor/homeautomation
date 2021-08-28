import threading
from device.deurbel_device import DeurbelGong, DeurbelKnop


class DeurbelGatewayException(Exception):
    def __init__(self, message):
        super(DeurbelGatewayException, self).__init__(message)


class DeurbelGateway:
    CONFIG_DEURBEL = 'deurbel'
    CONFIG_GONGDURATION = 'gong_duration_ms'
    CONFIG_GONGDURATION_DEFAULT = 1

    def __init__(self, config):
        self._knop = None
        self._gong = None
        self._ringing = False
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
        self._ringing = False

    def already_ringing(self):
        return self._ringing

    def someone_at_the_deur(self):
        if not (self._knop or self._gong):
            self.set_deurbel()
        if self._knop.is_ingedrukt():
            if self.already_ringing():
                # Returns only once if pressed during ringing
                return False
            else:
                t = threading.Thread(target=self.ringing)
                t.setDaemon(True)
                t.start()
                return True
        return False

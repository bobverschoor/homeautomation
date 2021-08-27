import threading
from sensor.deurbel_device import DeurbelGong, DeurbelKnop


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
        self._when_pressed = None
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
        self._gong.ring(self._gongduration)

    def someone_at_the_deur(self):
        if not (self._knop or self._gong):
            self.set_deurbel()
        if self._knop.is_ingedrukt():
            t = threading.Thread(target=self.ringing)
            t.setDaemon(True)
            t.start()
            return True
        else:
            return False

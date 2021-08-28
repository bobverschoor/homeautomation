import unittest

from deurbel import DeurbelController
from gateways.deurbel_gateway import DeurbelGateway


class MockDeurbelGateway(DeurbelGateway):
    def __init__(self, config):
        super().__init__(config)
        self.knop_ingedrukt = False
        self._knop = "iets"
        self._gong = "iets"

    def ringing(self):
        print("Er klinkt een geluid")

    def already_ringing(self):
        return False

    def knop_ingedrukt(self):
        return self.knop_ingedrukt

    def someone_at_the_deur(self):
        return True


class Deurbeltest(unittest.TestCase):

    def test_telegram_works(self):
        deurbelcontroller = DeurbelController('../../main/resources/secrets.ini')
        mockdeurbelgateway = MockDeurbelGateway({DeurbelGateway.CONFIG_DEURBEL: ""})
        deurbelcontroller._deurbel = mockdeurbelgateway
        deurbelcontroller._testing = True
        deurbelcontroller.control_loop()
        self.assertTrue(True)

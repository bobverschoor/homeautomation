import datetime
import unittest

from deurbel import DeurbelController
from device.telegram_device import TelegramDevice
from entiteiten.meetwaarde import Meetwaarde
from gateways.deurbel_gateway import DeurbelGateway
from gateways.messenger_gateway import MessengerGateway


class MockDeurbelGateway(DeurbelGateway):
    def __init__(self):
        super().__init__({DeurbelGateway.CONFIG_DEURBEL: ""})
        self.knop_ingedrukt = False
        self._knop = "iets"
        self._gong = "iets"

    def someone_at_the_deur(self):
        return Meetwaarde(eenheid='test', waarde=True, tags={})


class MockTelegram(TelegramDevice):
    def __init__(self):
        super().__init__({TelegramDevice.CONFIG_TELEGRAM: {TelegramDevice.CONFIG_TELEGRAM_TOKEN: "1459645932:AAGt",
                                                           TelegramDevice.CONFIG_TELEGRAM_CHANNEL_ID: "12158810"}})

    def message_send(self, message):
        return True


class MockMessenger(MessengerGateway):

    def __init__(self):
        super().__init__({})
        self._messengerdevice = MockTelegram()


class Deurbeltest(unittest.TestCase):

    def test_silence_window(self):
        deurbelcontroller = DeurbelController('../../main/resources/secrets.ini')
        mockdeurbelgateway = MockDeurbelGateway()
        deurbelcontroller._deurbel = mockdeurbelgateway
        deurbelcontroller._messenger = MockMessenger()
        now = datetime.datetime.now()
        deurbelcontroller._messenger._lastmessage_send = now
        deurbelcontroller.answer_door()
        self.assertEqual(now, deurbelcontroller._messenger._lastmessage_send)
        minute_ago = now - datetime.timedelta(seconds=61)
        deurbelcontroller._messenger._lastmessage_send = minute_ago
        deurbelcontroller.answer_door()
        self.assertNotEqual(minute_ago, deurbelcontroller._messenger._lastmessage_send)
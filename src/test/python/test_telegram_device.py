import unittest

from device.telegram_device import TelegramException, TelegramDevice
from mock_api import MockAPI


class TestTelegramDevice(unittest.TestCase):
    def test_telegram_setup(self):
        self.assertRaises(TelegramException, TelegramDevice, {})
        self.assertRaises(TelegramException, TelegramDevice, {TelegramDevice.CONFIG_TELEGRAM: {}})

    def test_send_message(self):
        tg = TelegramDevice({TelegramDevice.CONFIG_TELEGRAM: {TelegramDevice.CONFIG_TELEGRAM_TOKEN: "1459645932:AAGt",
                                                              TelegramDevice.CONFIG_TELEGRAM_CHANNEL_ID: "12158810"}})
        mock_api = MockAPI()
        tg._api = mock_api
        mock_api.json = testdata
        self.assertTrue(tg.message_send("Er staat iemand aan de voordeur."))


testdata = '{"ok":true,"result":{"message_id":2024,"sender_chat":{"id":-1001215881016,"title":"Ps5-alerter-nl",' \
           '"type":"channel"},"chat":{"id":-1001215881016,"title":"Ps5-alerter-nl","type":"channel"},' \
           '"date":1630146077,"text":"Er staat iemand aan de voordeur."}}'
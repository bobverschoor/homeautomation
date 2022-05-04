import datetime

from device.api import Api, ApiException


class TelegramException(Exception):
    def __init__(self, message):
        super(TelegramException, self).__init__(message)


class TelegramDevice:
    CONFIG_TELEGRAM = 'telegram'
    CONFIG_TELEGRAM_TOKEN = 'token'
    CONFIG_TELEGRAM_CHANNEL_ID = 'channel_id'
    BASE_URL = "https://api.telegram.org/bot"

    def __init__(self, config):
        if TelegramDevice.CONFIG_TELEGRAM in config:
            self._config = config[TelegramDevice.CONFIG_TELEGRAM]
            if TelegramDevice.CONFIG_TELEGRAM_TOKEN in self._config and \
                    TelegramDevice.CONFIG_TELEGRAM_CHANNEL_ID in self._config:
                token = self._config[TelegramDevice.CONFIG_TELEGRAM_TOKEN]
                self._channel_id = self._config[TelegramDevice.CONFIG_TELEGRAM_CHANNEL_ID]
            else:
                raise TelegramException("Config file section telegram missing " +
                                        TelegramDevice.CONFIG_TELEGRAM_TOKEN + " or " +
                                        TelegramDevice.CONFIG_TELEGRAM_CHANNEL_ID)
        else:
            raise TelegramException("Config file missing Telegram section.")
        url = TelegramDevice.BASE_URL + token + "/sendMessage"
        self._api = Api(url)
        self._message_send_date = -1

    def get_last_message_send(self):
        return self._message_send_date

    def message_send(self, message):
        body = {'chat_id': self._channel_id,
                'text': message}
        try:
            self._api.post_data(body)
            output = self._api.get_json()
            if 'ok' in output and output['ok']:
                self._message_send_date = datetime.datetime.now()
                return True
        except ApiException as e:
            print(e)
            return False

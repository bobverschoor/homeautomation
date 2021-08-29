import datetime


class MessengerGateway:
    CONFIG_SILENCE_WINDOW = 'silence_window'
    CONFIG_MESSENGER = 'messenger'
    CONFIG_TEXT_SOMEONE_AT_THE_DOOR = "text_someone_at_the_door"
    DEFAULT_TEXT_SOMEONE_AT_THE_DOOR = "Er staat iemand bij de voordeur."
    DEFAULT_SILENCE_WINDOW = 60

    def __init__(self, config, debug=False):
        self._messengerdevice = None
        self._debug = debug
        silence_window = MessengerGateway.DEFAULT_SILENCE_WINDOW
        text_someone_at_the_door = MessengerGateway.DEFAULT_TEXT_SOMEONE_AT_THE_DOOR
        if MessengerGateway.CONFIG_MESSENGER in config:
            config_section = config[MessengerGateway.CONFIG_MESSENGER]
            if MessengerGateway.CONFIG_SILENCE_WINDOW in config_section:
                silence_window = int(config_section[MessengerGateway.CONFIG_SILENCE_WINDOW])
            if MessengerGateway.CONFIG_TEXT_SOMEONE_AT_THE_DOOR in config_section:
                text_someone_at_the_door = config_section[MessengerGateway.CONFIG_TEXT_SOMEONE_AT_THE_DOOR]
        self._lastmessage_send = datetime.datetime.now()
        self._silence_window = silence_window
        self._text_someone_at_the_door = text_someone_at_the_door

    def setup(self, messenger):
        self._messengerdevice = messenger

    def allowed_to_send(self):
        silence_period = datetime.datetime.now() - self._lastmessage_send
        silence_period = int(silence_period.total_seconds())
        if silence_period > self._silence_window:
            return True
        else:
            return False

    def send_text_someone_at_the_door(self):
        if not self._messengerdevice:
            raise ModuleNotFoundError("Messenger not initialised")
        if self.allowed_to_send():
            if self._messengerdevice.message_send(self._text_someone_at_the_door):
                self._lastmessage_send = datetime.datetime.now()
                if self._debug:
                    print("Sending last message at: " + str(self._lastmessage_send))

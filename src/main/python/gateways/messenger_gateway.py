class MessengerGateway:

    def __init__(self):
        self._messengerdevice = None

    def setup(self, messenger):
        self._messengerdevice = messenger

    def send(self, message):
        if not self._messengerdevice:
            ModuleNotFoundError("Messenger not initialised")
        self._messengerdevice.send_message(message)
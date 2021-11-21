class User:
    CONFIG_CHAT_ID = 'chat_id'
    CONFIG_USERNAME = 'username'
    CONFIG_MAC_ADDRESSES = 'mac_addresses'

    def __init__(self, userconfig):
        if User.CONFIG_CHAT_ID in userconfig and User.CONFIG_USERNAME in userconfig and \
                User.CONFIG_MAC_ADDRESSES in userconfig:
            self._chat_id = userconfig[User.CONFIG_CHAT_ID]
            self._username = userconfig[User.CONFIG_USERNAME]
            self._mac_adresses = []
            for macadres in userconfig[User.CONFIG_MAC_ADDRESSES].split(','):
                macadres = macadres.strip()
                self._mac_adresses.append(macadres)

    @property
    def chat_id(self):
        return self._chat_id

    @property
    def name(self):
        return self._username

    @property
    def macadresses(self):
        return self._mac_adresses

import json

import requests


class ApiException(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message


class Api:
    def __init__(self, url, payload):
        self._url = url
        self._payload = payload
        self.json = {}

    def request_data(self):
        try:
            weer = requests.get(self._url, params=self._payload, timeout=30)
            if weer.status_code == 200:
                self.json = json.loads(weer.text)
            else:
                raise ApiException("Api status code not 200: " + str(weer.status_code) + weer.text)
        except TimeoutError:
            raise ApiException("Api does not respond in 30 seconds: " + self._url)

    def get_json(self):
        if self.json == {}:
            raise ApiException("Json not loaded, try request data first.")
        return self.json

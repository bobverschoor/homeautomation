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
        self.text_output = ""

    def request_data(self):
        try:
            weer = requests.get(self._url, params=self._payload, timeout=30)
            if weer.status_code == 200:
                self.text_output = weer.text
            else:
                raise ApiException("Api status code not 200: " + str(weer.status_code) + weer.text)
        except TimeoutError:
            raise ApiException("Api does not respond in 30 seconds: " + self._url)

    def get_text_output(self):
        return self.text_output

    def get_json(self):
        if self.text_output == "":
            raise ApiException("Text not loaded, try request data first.")
        self.json = json.loads(self.text_output)
        return self.json

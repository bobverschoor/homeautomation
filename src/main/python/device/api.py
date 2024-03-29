import json
import requests
from requests import RequestException


class ApiException(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message


class Api:
    def __init__(self, url, payload="", expected_startsymbol='{'):
        self._url = url
        self._payload = payload
        self._expected_startsymbol_output = expected_startsymbol
        self.json = {}
        self.text_output = ""

    def download_nr_of_bytes_elapsed_time(self):
        r = requests.get(self._url, params=self._payload)
        return int(r.headers['Content-Length']), r.elapsed.total_seconds()

    def request_data(self):
        try:
            self.handle_result(requests.get(self._url, params=self._payload, timeout=30))
        except TimeoutError:
            raise ApiException("Api does not respond in 30 seconds: " + self._url)
        except RequestException as e:
            raise ApiException("No connection to Api: " + self._url + "\n" + str(e))

    def post_data(self, body, additionalpath=""):
        try:
            url = self._url + additionalpath
            self.handle_result(requests.post(url, data=body, timeout=30))
        except TimeoutError:
            raise ApiException("Api does not respond in 30 seconds: " + self._url)
        except RequestException as e:
            raise ApiException("No connection to Api: " + self._url + "\n" + str(e))

    def put_data(self, body, additionalpath=""):
        try:
            url = self._url + additionalpath
            self.handle_result(requests.put(url, data=body, timeout=30))
        except TimeoutError:
            raise ApiException("Api does not respond in 30 seconds: " + self._url)

    def handle_result(self, result):
        if result.status_code == 200:
            if self._expected_startsymbol_output:
                if result.text.startswith(self._expected_startsymbol_output):
                    self.text_output = result.text
                else:
                    raise ApiException("Api not expected output: " + str(self._url) + "\n" + result.text)
            else:
                self.text_output = result.text
        else:
            raise ApiException("Api status code not 200: " + str(result.status_code) + result.text)

    def get_text_output(self):
        return self.text_output

    def get_json(self):
        if self.text_output == "":
            raise ApiException("Text not loaded, try request or post data first.")
        self.json = json.loads(self.text_output)
        return self.json

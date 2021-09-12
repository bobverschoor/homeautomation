import json

from device.api import Api


class MockAPI(Api):
    def __init__(self, url=""):
        super().__init__(url, "")
        self.json = ""
        self.text_output = ""
        self.record = []

    def request_data(self):
        pass

    def post_data(self, body, additionalpath=""):
        pass

    def put_data(self, body, additionalpath=""):
        self.record.append(str(self._url) + additionalpath + "?" + str(body))

    def get_json(self):
        return json.loads(self.json)

    def get_text_output(self):
        return self.text_output

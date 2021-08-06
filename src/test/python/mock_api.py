import json

from sensor.api import Api


class MockAPI(Api):
    def __init__(self):
        super().__init__("", "")
        self.json = ""
        self.text_output = ""

    def request_data(self):
        pass

    def get_json(self):
        return json.loads(self.json)

    def get_text_output(self):
        return self.text_output
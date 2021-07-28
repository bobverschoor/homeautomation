import json

from sensor.api import Api


class MockAPI(Api):
    def __init__(self):
        super().__init__("", "")
        self.json = ""

    def request_data(self):
        pass

    def get_json(self):
        return json.loads(self.json)

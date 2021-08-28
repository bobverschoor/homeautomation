import json

from device.api import Api


class MockAPI(Api):
    def __init__(self):
        super().__init__("", "")
        self.json = ""
        self.text_output = ""

    def request_data(self):
        pass

    def post_data(self, body):
        pass

    def get_json(self):
        return json.loads(self.json)

    def get_text_output(self):
        return self.text_output

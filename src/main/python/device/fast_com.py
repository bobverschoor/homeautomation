import re
from timeit import default_timer as timer

from device.api import Api


def parse_for_url(text):
    return re.findall(r'<script src="(.+?)"',text)


def parse_token(text):
    tokenmatch = re.search(r'token:"(.+?)"', text)
    if tokenmatch is None:
        return ""
    else:
        return tokenmatch.group(1)


class FastComDevice:
    TOKEN_URL = 'fast_com_token_url'
    SPEEDTEST_URL = 'fast_com_speedtest_url'

    def __init__(self, config):
        self._config = config
        self.type = "fast_com"
        self._token_url = None
        self._url = None
        self._download_b_s = -1
        self._latency_ms = -1

    def loaded(self):
        if FastComDevice.TOKEN_URL in self._config:
            self._token_url = self._config[FastComDevice.TOKEN_URL]
        else:
            return False
        if FastComDevice.SPEEDTEST_URL in self._config:
            self._url = self._config[FastComDevice.SPEEDTEST_URL]
        else:
            return False
        return True

    def get_download_speed(self):
        if self._download_b_s == -1:
            self._speedresults()
        return self._download_b_s

    def get_ping_speed(self):
        if self._latency_ms == -1:
            self._speedresults()
        return self._latency_ms

    def _speedresults(self):
        token = self._get_token()
        targets = self._get_targets(self._url, token)
        download_times = []
        latency_times = []
        for target in targets:
            start = timer()
            nr_of_bytes, latency = self._get_downloadbytes_latency(target['url'], token)
            end = timer()
            total_time = end - start
            bytes_sec = nr_of_bytes/total_time
            download_times.append(bytes_sec)
            latency_times.append(latency)
        self._download_b_s = average_list(download_times)
        self._latency_ms = average_list(latency_times)

    def _get_downloadbytes_latency(self, url, token):
        params = {"https": True, "token": token}
        api = Api(url=url, payload=params)
        return api.download_nr_of_bytes_elapsed_time()

    def _get_targets(self, url, token):
        params = {"https": True, "urlCount": 3, "token": token}
        api = Api(url=url, payload=params)
        api.request_data()
        return api.get_json()['targets']

    def _get_token(self):
        # token zit verstopt in een gegenereerde js file
        token = ""
        api = Api(url=self._token_url, expected_startsymbol='<')
        api.request_data()
        for jsonfile_url in parse_for_url(api.get_text_output()):
            api = Api(url=self._token_url + jsonfile_url, expected_startsymbol='!')
            api.request_data()
            token = parse_token(api.get_text_output())
            if token != "":
                break
        return token


def average_list(av_list):
    av = 0
    for el in av_list:
        av += el
    return av / len(av_list)


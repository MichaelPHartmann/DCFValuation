import datetime
import requests
import os

SANDBOX = False

class iexCloud():

    def _iex_init(self):
        self.lastRequest = None
        self.lastRequestTime = None
        self.raw = None

        if SANDBOX:
            self.IEX_STOCK_BASE_URL = 'https://sandbox.iexapis.com/beta/stock/'
        else:
            self.IEX_STOCK_BASE_URL = 'https://cloud.iexapis.com/beta/stock/'

    def _append_iex_token(self, url):
        token = str(os.getenv('IEX_TOKEN'))
        return f"{url}&token={token}"

    def _get_iex_json_request(self, url):
        url = append_iex_token(url)
        print(url)
        result = requests.get(url)
        if result.status_code != 200:
            print(result)
            raise BaseException(result.text)
        self.raw = result.json()
        self.lastRequest = url
        self.lastRequestTime = datetime.datetime.now()

    def _replace_url_var(self, url, **kwargs):
        for key, value in kwargs.items():
            url = url.replace('{' + key + '}', value)
        return url

    def _make_request(self, url, **kwargs):
        url_formatted = self._replace_url_var(url, **kwargs)
        self._get_iex_json_request(url_formatted)

    def make_request(self):
        raise ImplementationError("make_request")


def append_iex_token(url):
    token = os.getenv('IEX_TOKEN')
    return f"{url}&token={token}"

def get_iex_json_request(url):
    url = append_iex_token(url)
    result = requests.get(url)
    if result.status_code != 200:
        raise BaseException(result.text)
    result = result.json()
    return result

def replace_url_var(url, **kwargs):
    for key, value in kwargs.items():
        url = url.replace('{' + key + '}', value)
    return url

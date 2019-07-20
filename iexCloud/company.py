from iexCloud.iexCloud import iexCloud


class Company(iexCloud):

    def __init__(self, symbol):
        self._iex_init()
        self.URL = self.IEX_STOCK_BASE_URL + '{symbol}/company?'
        self.symbol = symbol
        self.make_request()

    def make_request(self):
        self._make_request(self.URL, symbol=self.symbol)

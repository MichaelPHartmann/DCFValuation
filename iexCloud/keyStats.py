from iexCloud.iexCloud import iexCloud


class KeyStats(iexCloud):


    def __init__(self, symbol, stat=None):
        self._iex_init()
        self.URL = self.IEX_STOCK_BASE_URL + '{symbol}/stats'
        self.symbol = symbol
        self.make_request(stat)

    def make_request(self, stat=None):
        url = self.URL
        if stat: url += f'/{stat}'
        url += '?'
        self._make_request(url, symbol=self.symbol)

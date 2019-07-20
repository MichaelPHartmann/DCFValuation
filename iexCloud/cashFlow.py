from iexCloud.iexCloud import iexCloud


class CashFlow(iexCloud):

    def __init__(self, symbol, last=None, field=None, period=None):
        self._iex_init()
        self.URL = self.IEX_STOCK_BASE_URL + '{symbol}/cash-flow'
        self.symbol = symbol
        self.make_request(last, field, period)

    def make_request(self, last=None, field=None, period=None):
        url = self.URL
        if last: url += f'/{last}'
        if field: url += f'{field}'
        if period: url += f'/period={period}'
        url += '?'
        self._make_request(url, symbol=self.symbol)
        if last: assert( len(self.raw['cashflow']) == last )

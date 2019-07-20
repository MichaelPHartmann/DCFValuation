from iexCloud.iexCloud import iexCloud


class IncomeStatement(iexCloud):

    def __init__(self, symbol, last=None, field=None, period=None):
        self._iex_init()
        self.URL = self.IEX_STOCK_BASE_URL + '{symbol}/income'
        self.symbol = symbol
        self.make_request(last, field, period)

    def make_request(self, last=None, field=None, period=None):
        url = self.URL
        if last: url += f'/{last}'
        if field: url += f'{field}'
        if period: url += f'/period={period}'
        url += '?'
        self._make_request(url, symbol=self.symbol)
        self.last = len(self.raw['income'])
        if last: assert( self.last == last )

    def get_avg_revenue_growth(self):
        arg = 0
        for i in range(self.last-1):
            arg += (self.raw['income'][i]['totalRevenue'] / self.raw['income'][i+1]['totalRevenue']) - 1
        return arg

    def get_avg_operating_margin(self):
        aom = 0
        for i in range(self.last):
            aom += self.raw['income'][i]['operatingIncome'] / self.raw['income'][i]['totalRevenue']
        return aom

    def get_avg_tax_rate(self):
        atr = 0
        for i in range(self.last):
            atr += self.raw['income'][i]['incomeTax'] / self.raw['income'][i]['pretaxIncome']
        return atr

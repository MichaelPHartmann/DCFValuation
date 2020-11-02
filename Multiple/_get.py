from FinMesh.iex import stock
import math

class companyMultiplesAnalysis():
# Base class from which target and peer companies are defined.

    def __init__(self,ticker):
        self.ticker = ticker
        self.price = stock.price(ticker)
        self.incomeStatement = self.statement_sanitizer('income')
        self.balanceSheet = self.statement_sanitizer('balance')
        self.cashFlowStatement = self.statement_sanitizer('cash')
        print(self.cashFlowStatement)
        if self.cashFlowStatement is None:
            pass
        else:
            self.sharesOutstanding = self.balanceSheet['commonStock']
            self.marketCap = self.sharesOutstanding * self.price
            self.revenueTTM = self.trailing_twelve_income('totalRevenue')
            self.ebitdaTTM = self.trailing_twelve_income('ebit') - self.trailing_twelve_cashflow('depreciation')
            self.netIncomeTTM = self.trailing_twelve_income('netIncome')
            self.cashFlowTTM = self.trailing_twelve_cashflow('cashFlow')
            self.enterpiseValue = self.enterpise_value()
            self.bookValue = self.book_value()

            self.priceEarnings = self.price / (self.netIncomeTTM / self.sharesOutstanding)
            self.priceRevenue = self.price / (self.revenueTTM / self.sharesOutstanding)
            self.enterpriseEBITDA = self.enterpiseValue / self.ebitdaTTM
            self.enterpriseRevenue = self.enterpiseValue / self.revenueTTM
            self.priceBook = self.price / (self.bookValue / self.sharesOutstanding)
            self.priceCashFlow = self.price / (self.cashFlowTTM / self.sharesOutstanding)

    def statement_sanitizer(self, statement):
        if statement == 'income':
            result = stock.income_statement(self.ticker, last=4)['income']
            for quarter in result:
                for key in quarter:
                    if quarter[key] is None:
                        quarter[key] = 0
                    else:
                        pass
            return result

        if statement == 'balance':
            result = stock.balance_sheet(self.ticker)['balancesheet']
            if len(result) == 0:
                self.balanceSheet = None
            else:
                result = result[0]
                for key in result:
                    if result[key] is None:
                        result[key] = 0
                    else:
                        pass
                return result

        if statement == 'cash':
            result = stock.cash_flow(self.ticker, last=4)['cashflow']
            for quarter in result:
                for key in quarter:
                    if quarter[key] is None:
                        quarter[key] = 0
                    else:
                        pass
            return result

    def trailing_twelve_income(self, account):
        ttm = 0
        for q in range(len(self.incomeStatement)-1):
            ttm += self.incomeStatement[q][account]
        return ttm

    def trailing_twelve_cashflow(self, account):
        ttm = 0
        for q in range(len(self.cashFlowStatement)-1):
            ttm += self.cashFlowStatement[q][account]
        return ttm

    def enterpise_value(self):
        total_debt = self.balanceSheet['currentLongTermDebt'] + self.balanceSheet['longTermDebt']
        result = self.marketCap + total_debt - self.balanceSheet['currentCash']
        return result

    def book_value(self):
        if self.balanceSheet['intangibleAssets'] is None:
            intangibleAssets = 0
        else:
            intangibleAssets = self.balanceSheet['intangibleAssets']
        result = self.balanceSheet['totalAssets'] - intangibleAssets - self.balanceSheet['totalLiabilities']
        return result


class targetMultiplesAnalysis(companyMultiplesAnalysis):

    def __init__(self,ticker):
        super().__init__(ticker)
        self.peers = stock.peers(ticker)
        self.numpeers = len(self.peers)

    def value_weighting(self,x,w):
        return x * w

    def peer_comparison(self):
        print(self.peers)
        total_marketcap = 0
        MC = []
        W = []
        PE = []
        PR = []
        EE = []
        ER = []
        PB = []
        PC = []
        with open(f'{self.ticker}.csv', 'w') as f:
            header = 'Ticker,MarketCap,P/E,P/S,EV/EBITDA,EV/S,P/B,P/CF\n'
            firstline = f'{self.ticker},{self.marketCap},{self.priceEarnings},{self.priceRevenue},{self.enterpriseEBITDA},{self.enterpriseRevenue},{self.priceBook},{self.priceCashFlow}\n'
            f.write(header)
            f.write(firstline)
            # This writes individual stock multiples data to the CSV file
            for n in self.peers:
                n = companyMultiplesAnalysis(n)
                total_marketcap += n.marketCap
                MC.append(n.marketCap)
                PE.append(n.priceEarnings)
                PR.append(n.priceRevenue)
                EE.append(n.enterpriseEBITDA)
                ER.append(n.enterpriseRevenue)
                PB.append(n.priceBook)
                PC.append(n.priceCashFlow)
                line = f'{n.ticker},{n.marketCap},{n.priceEarnings},{n.priceRevenue},{n.enterpriseEBITDA},{n.enterpriseRevenue},{n.priceBook},{n.priceCashFlow}\n'
                f.write(line)
            # Here we are weighting all the values according to market cap to prepare for appending to the CSV file
            for i in MC:
                W.append(i / total_marketcap)
            PE = list(map(self.value_weighting,PE,W))
            PR = list(map(self.value_weighting,PE,W))
            EE = list(map(self.value_weighting,PE,W))
            ER = list(map(self.value_weighting,PE,W))
            PB = list(map(self.value_weighting,PE,W))
            PC = list(map(self.value_weighting,PE,W))
            final_line = f'Peer Average,{total_marketcap/self.numpeers},{sum(PE)},{sum(PR)},{sum(EE)},{sum(ER)},{sum(PB)},{sum(PC)}'
            f.write(final_line)

AAPL = targetMultiplesAnalysis('MSFT')
AAPL.peer_comparison()

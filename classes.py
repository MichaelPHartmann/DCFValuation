import os
import sys
PATH_TO_API = os.path.abspath("../FinMesh")
sys.path.insert(0, PATH_TO_API)
import iex.stock
import usgov.yieldcurve

# Establishes a class for income statements, feeds DCFSymbol
class incomeStatement:
    def __init__(self, symbol):
        self.incomestatement = iex.stock.income_statement(symbol)
        self.reportDate = self.incomestatement['reportDate']
        self.totalRevenue = self.incomestatement['totalRevenue']
        self.costOfRevenue = self.incomestatement['costOfRevenue']
        self.grossProfit = self.incomestatement['grossProfit']
        self.researchAndDevelopment = self.incomestatement['researchAndDevelopment']
        self.sellingGeneralAndAdmin = self.incomestatement['sellingGeneralAndAdmin']
        self.operatingExpense = self.incomestatement['operatingExpense']
        self.operatingIncome = self.incomestatement['operatingIncome']
        self.otherIncomeExpenseNet = self.incomestatement['otherIncomeExpenseNet']
        self.ebit = self.incomestatement['ebit']
        self.interestIncome = self.incomestatement['interestIncome']
        self.pretaxIncome = self.incomestatement['pretaxIncome']
        self.incomeTax = self.incomestatement['incomeTax']
        self.minorityInterest = self.incomestatement['minorityInterest']
        self.netIncome = self.incomestatement['netIncome']
        self.netIncomeBasic = self.incomestatement['netIncomeBasic']

# Establishes a class for balance sheets, feeds DCFSymbol
class balanceSheet:
    def __init__(self, symbol):
        self.reportDate
        self.currentCash
        self.shortTermInvestments
        self.receivables
        self.inventory
        self.otherCurrentAssets
        self.currentAssets
        self.longTermInvestments
        self.propertyPlantEquipment
        self.goodwill
        self.intangibleAssets
        self.otherAssets
        self.totalAssets
        self.accountsPayable
        self.currentLongTermDebt
        self.otherCurrentLiabilities
        self.totalCurrentLiabilities
        self.longTermDebt
        self.otherLiabilities
        self.minorityInterest
        self.totalLiabilities
        self.commonStock
        self.retainedEarnings
        self.treasuryStock
        self.capitalSurplus
        self.shareholderEquity
        self.netTangibleAssets

# Establishes a class for cash flow statements, feeds DCFSymbol
class cashFlow:
    def __init__(self, symbol):
        self.reportDate
        self.netIncome
        self.depreciation
        self.changesInReceivables
        self.changesInInventories
        self.cashChange
        self.cashFlow
        self.capitalExpenditures
        self.investments
        self.investingActivityOther
        self.totalInvestingCashFlows
        self.dividendsPaid
        self.netBorrowings
        self.otherFinancingCashFlows
        self.cashFlowFinancing
        self.exchangeRateEffect


# Establishes a class for key statistics, feeds DCFSymbol
class keyStats:
    def __init__(self, symbol):
        self.week52change
        self.week52high
        self.week52low
        self.marketcap
        self.employees
        self.day200MovingAvg
        self.day50MovingAvg
        self.float
        self.avg10Volume
        self.avg30Volume
        self.ttmEPS
        self.ttmDividendRate
        self.companyName
        self.sharesOutstanding
        self.maxChangePercent
        self.year5ChangePercent
        self.year2ChangePercent
        self.year1ChangePercent
        self.ytdChangePercent
        self.month6ChangePercent
        self.month3ChangePercent
        self.month1ChangePercent
        self.day30ChangePercent
        self.day5ChangePercent
        self.nextDividendDate
        self.dividendYield
        self.nextEarningsDate
        self.exDividendDate
        self.peRatio
        self.beta

# Creates a class for companies to lay out their financial information
class Company:
    def __init__(self, symbol):
        self.price
        self.income_statement = iex.stock.income_statement(symbol, period='annual', last=4)
        self.balance_sheet = iex.stock.balance_sheet(symbol, period='annual', last=4)
        self.cash_flow = iex.stock.cash_flow(symbol, period='annual', last=4)
        self.key_stats = iex.stock.key_stats(symbol)

import os
import sys
PATH_TO_API = os.path.abspath("../FinMesh")
sys.path.insert(0, PATH_TO_API)
import iex.stock
import usgov.yieldcurve

# Establishes a class for income statements, feeds DCFSymbol
class incomeStatement:
    def __init__(self, symbol):
        self.revenue

# Establishes a class for balance sheets, feeds DCFSymbol
class balanceSheet:
    def __init__(self, symbol):
        self.cash

# Establishes a class for cash flow statements, feeds DCFSymbol
class cashFlow:
    def __init__(self, symbol):
        self.capex

# Establishes a class for key statistics, feeds DCFSymbol
class keyStats:
    def __init__(self, symbol):
        self.shares_outstanding

# Creates a class for companies to lay out their financial information
class Company:
    def __init__(self, symbol):
        self.price
        self.income_statement = iex.stock.income_statement(symbol, period='annual', last=4)
        self.balance_sheet = iex.stock.balance_sheet(symbol, period='annual', last=4)
        self.cash_flow = iex.stock.cash_flow(symbol, period='annual', last=4)
        self.key_stats = iex.stock.key_stats(symbol)

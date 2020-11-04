from FinMesh.iex import stock
from FinMesh import usgov
import pandas as pd
import xlsxwriter as xlw

def create_corporate_book(ticker):


    IS = stock.income_statement(ticker, period='annual', last=4)['income']
    BS = stock.balance_sheet(ticker, period='annual', last=4)['balancesheet']
    CS = stock.cash_flow(ticker, period='annual', last=4)['cashflow']
    P = stock.price(ticker)
    Rf = usgov.get_yield()['10year']

    workbook = xlw.Workbook(f'{ticker}_Valuation_Build.xlsx')
    statements = workbook.add_worksheet(f'Financial Statements')

    row = 0
    col = 0
    # Write Income Statement Data
    statements.write(row,col,'Income Statement')
    row += 1
    for key in IS[0]:
        statements.write(row, col, key)
        statements.write(row, col+1, IS[0][key])
        statements.write(row, col+2, IS[1][key])
        statements.write(row, col+3, IS[2][key])
        statements.write(row, col+4, IS[3][key])
        row += 1
"""
    # Write Balance Sheet Data
    statements.write(row,col,'Balance Sheet')
    row += 1
    for key in BS[0]:
        statements.write(row, col, key)
        statements.write(row, col+1, IS[0][key])
        statements.write(row, col+2, IS[1][key])
        statements.write(row, col+3, IS[2][key])
        statements.write(row, col+4, IS[3][key])
        row += 1

    # Write Cash Flow Statement Data
    statements.write(row,col,'Cash Flow Statement')
    row += 1
    for key in CS[0]:
        statements.write(row, col, key)
        statements.write(row, col+1, IS[0][key])
        statements.write(row, col+2, IS[1][key])
        statements.write(row, col+3, IS[2][key])
        statements.write(row, col+4, IS[3][key])
        row += 1"""

#workbook.close()

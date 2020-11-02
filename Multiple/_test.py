from FinMesh.iex import stock
from FinMesh import usgov
import pandas as pd
import xlsxwriter as xlw

company = 'AMD'

IS = stock.income_statement(company, period='annual', last=4)['income']
BS = stock.balance_sheet(company, period='annual', last=4)['balancesheet']
CS = stock.cash_flow(company, period='annual', last=4)['cashflow']
P = stock.price(company)
Rf = usgov.get_yield()['10year']


"""
with open(f'{company}_Financial_statement.csv', 'w') as statement:
    statement.write('Ticker, Current Price, Risk Free Rate\n')
    statement.write(f'{company},{P},{Rf}\n')
    statement.write('Income Statement\n')
    for key in IS[0]:
        statement.write(f'{key},')
    statement.write('\n')
    for quarter in IS:
        for key in quarter:
            statement.write(str(quarter[key])+',')
        statement.write('\n')

    statement.write('Balance Sheet\n')
    for key in BS:
        statement.write(f'{key},')
    statement.write('\n')
    for key in BS:
        statement.write(str(BS[key])+',')
    statement.write('\n')

    statement.write('Cash Flow Statement\n')
    for key in CS[0]:
        statement.write(f'{key},')
    statement.write('\n')
    for quarter in CS:
        for key in quarter:
            statement.write(str(quarter[key])+',')
        statement.write('\n')
"""

workbook = xlw.Workbook(f'{company}_Valuation_Build.xlsx')
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

# Write Balance Sheet Data
statements.write(row,col,'Balance Sheet')
row += 1
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
row += 1
for key in CS[0]:
    statements.write(row, col, key)
    statements.write(row, col+1, IS[0][key])
    statements.write(row, col+2, IS[1][key])
    statements.write(row, col+3, IS[2][key])
    statements.write(row, col+4, IS[3][key])
    row += 1

workbook.close()

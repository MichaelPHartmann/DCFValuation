import os
import sys
PATH_TO_API = os.path.abspath("../iexfinancepy")
sys.path.insert(0, PATH_TO_API)
import iex.stock
import usgov.yieldcurve
from bs4 import BeautifulSoup as bs
import requests

VERBOSE = True

def vprint(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

LAST_YEARS = 4
MODEL_LENGTH = 5
DAMODARAN_URL = 'http://pages.stern.nyu.edu/~adamodar/'

# TODO estimate beta
def beta(symbol):
    return 1.5

# TODO: estimate erp
def erp():
    0.05

# TODO: estimate wacc
def wacc(symbol, creditRating):
    income_statement = iex.stock.income_statement(symbol, period='annual', last=LAST_YEARS)
    balance_sheet = iex.stock.balance_sheet(symbol, period='annual', last=LAST_YEARS)
    key_stats = iex.stock.key_stats(symbol)
    current_price = iex.stock.price(symbol)
    risk_free = usgov.yieldcurve.get_yield()['10year']
    equity_premium = erp()
    company_beta = beta(symbol)
    spreads = {
    'aaa': 0.0075,
    'aa2': 0.010,
    'a1' : 0.0125,
    'a2' : 0.0138,
    'a3' : 0.0156,
    'baa2' : 0.02,
    'ba1' : 0.03,
    'ba2' : 0.036,
    'b1' : 0.045,
    'b2' : 0.054,
    'b3' : 0.066,
    'caa' : 0.09,
    'ca2' : 0.1108,
    'c2' : 0.1454,
    'd2' : 0.1938,
    }
    default_spread = spreads[creditRating]
    tax_rate = income_statement['income'][0]['incomeTax'] / income_statement['income'][0]['pretaxIncome']
    current_debt = balance_sheet['balancesheet'][0]['longTermDebt']
    current_shares_outstanding = key_stats['sharesOutstanding']
    market_equity = current_shares_outstanding * current_price
    percent_debt = current_debt / (market_equity + current_debt)
    percent_equity = current_equity / (market_equity + current_debt)
    equity_risk = equity_premium * beta

    return market_equity

# TODO: estimate terminal wacc
def terminal_wacc():
    return 0.11

def dcf_2(symbol, creditRating):
    # brings in json data from iex finance module
    income_statement = iex.stock.income_statement(symbol, period='annual', last=LAST_YEARS)
    balance_sheet = iex.stock.balance_sheet(symbol, period='annual', last=LAST_YEARS)
    cash_flow = iex.stock.cash_flow(symbol, period='annual', last=LAST_YEARS)
    key_stats = iex.stock.key_stats(symbol)

    # assertains that there are 4 years of data
    assert(len(cash_flow['cashflow']) == LAST_YEARS) #, "Not enough data")
    assert(len(income_statement['income']) == LAST_YEARS) #, "Not enough data")
    assert(len(balance_sheet['balancesheet']) == LAST_YEARS) #, "Not enough data")

    # reference before assignment
    average_revenue_growth = 0
    average_operating_margin = 0
    average_tax_rate = 0
    average_capex_ratio = 0

    # computes averages
    for i in range(LAST_YEARS-1):
        average_revenue_growth += (income_statement['income'][i]['totalRevenue'] / income_statement['income'][i+1]['totalRevenue']) - 1
        average_operating_margin += income_statement['income'][i]['operatingIncome'] / income_statement['income'][i]['totalRevenue']
        average_tax_rate += income_statement['income'][i]['incomeTax'] / income_statement['income'][i]['pretaxIncome']
        average_capex_ratio += cash_flow['cashflow'][i]['capitalExpenditures'] / income_statement['income'][i]['totalRevenue']
    average_revenue_growth /= LAST_YEARS - 1
    average_operating_margin /= LAST_YEARS - 1
    average_tax_rate /= LAST_YEARS - 1
    average_capex_ratio /= LAST_YEARS - 1

    # current values for 'base year'
    current_revenue = income_statement['income'][0]['totalRevenue']
    current_operating_income = income_statement['income'][0]['operatingIncome']
    current_tax_paid = income_statement['income'][0]['incomeTax']
    current_tax_adjusted_income = current_operating_income - current_tax_paid
    current_capex = cash_flow['cashflow'][0]['capitalExpenditures']
    current_cash_flow = cash_flow['cashflow'][0]['cashFlow']
    current_operating_margin = current_operating_income / current_revenue
    current_debt = balance_sheet['balancesheet'][0]['longTermDebt']
    current_cash = (balance_sheet['balancesheet'][0]['currentCash'] + balance_sheet['balancesheet'][0]['shortTermInvestments'])
    current_shares_outstanding = key_stats['sharesOutstanding']

    pf_revenues = [current_revenue]
    for a in range(MODEL_LENGTH):
        next_revenue = pf_revenues[a] * (1 + average_revenue_growth)
        pf_revenues.append(next_revenue)
    vprint(pf_revenues)

    wacc_yearly = [wacc(symbol, creditRating)]
    for n in range(MODEL_LENGTH):
        next_wacc = wacc_yearly[(len(wacc_yearly)-1)] - ((wacc()-terminal_wacc())/MODEL_LENGTH)
        wacc_yearly.append(next_wacc)
    vprint(wacc_yearly)

    discount_factor = []
    for d in range(MODEL_LENGTH):
        if len(discount_factor) == 0:
            next_discount_factor = (1/(1+wacc_yearly[d]))
            discount_factor.append(next_discount_factor)
        else:
            next_discount_factor = discount_factor[(len(discount_factor)-1)] * (1/(1+wacc_yearly[d]))
            discount_factor.append(next_discount_factor)
    vprint(discount_factor)

    # MAIN CALCULATIONS
    # for each year of the model this calculates present value and adds it to a list
    yearly_pv = []
    for r in pf_revenues[1:]:
        next_op_marg = r * average_operating_margin
        next_ta_income = next_op_marg * (1-average_tax_rate)
        next_reinvestment = r * average_capex_ratio
        next_fcff = next_ta_income - next_reinvestment
        next_pv = next_fcff * discount_factor[len(yearly_pv)-1]
        yearly_pv.append(next_pv)
    vprint(yearly_pv)

    # sums the list of present values
    cumulative_present_value = 0
    for p in yearly_pv:
        cumulative_present_value += p
    vprint(cumulative_present_value)

    # adds/subtracts from cumulative present value
    equity_value = cumulative_present_value + current_cash - current_debt

    # divides by shares outstanding
    value_per_share = equity_value / current_shares_outstanding
    vprint(value_per_share)


"""
def dcf(symbol):
    income_statement = iex.stock.income_statement(symbol, period='annual', last=LAST_YEARS)
    balance_sheet = iex.stock.balance_sheet(symbol, period='annual', last=LAST_YEARS)
    cash_flow = iex.stock.cash_flow(symbol, period='annual', last=LAST_YEARS)

    # assertains that there are 4 years of data
    assert(len(cash_flow['cashflow']) == LAST_YEARS)#, "Not enough data")
    assert(len(income_statement['income']) == LAST_YEARS)#, "Not enough data")
    assert(len(balance_sheet['balance_sheet']) == LAST_YEARS)#, "Not enough data")

    # computes averages
    for i in range(LAST_YEARS-1):
        average_revenue_growth += (income_statement['income'][i]['totalRevenue'] / income_statement['income'][i+1]['totalRevenue']) - 1
        average_operating_margin += income_statement['income'][i]['operatingIncome'] / income_statement['income'][i]['totalRevenue']
        average_tax_rate += income_statement['income'][i]['incomeTax'] / income_statement['income'][i]['pretaxIncome']
        capex_ratio += cash_flow['cashflow'][i]['capitalExpenditures'] / income_statement['income'][i]['totalRevenue']
    average_revenue_growth /= LAST_YEARS - 1
    average_operating_margin /= LAST_YEARS - 1
    average_tax_rate /= LAST_YEARS - 1
    average_capex_ratio /= LAST_YEARS - 1

    # current values for 'base year'
    current_revenue = income_statement['income'][0]['totalRevenue']
    current_operating_income = income_statement['income'][0]['operatingIncome']
    current_tax_paid = income_statement['income'][0]['incomeTax']
    current_tax_adjusted_income = current_operating_income - current_tax_paid
    current_capex = cash_flow['cashflow'][0]['capitalExpenditures']
    current_cash_flow = cash_flow['cashflow'][0]['cashFlow']
    current_operating_margin = current_operating_margin / current_revenue

    # calculates pro-forma revenues based on average revenue growth
    pf_revenues = [current_revenue]
    for a in range(MODEL_LENGTH):
        next_revenue = pf_revenues[a] * (1 + average_revenue_growth)
        pf_revenues.append(next_revenue)
    vprint(pf_revenues)

    # calculates pro-forma operating income based on average operating income
    pf_op_income = [current_operating_income]
    for b in pf_revenues[1:]:
        next_op_income = b * average_operating_margin
        pf_op_income.append(next_op_income)
    vprint(pf_op_income)

    # calculates pro-forma tax-adjusted income based on average tax rate
    pf_ta_income = [current_tax_adjusted_income]
    for c in pf_op_income[1:]:
        next_ta_income = c * (1 - average_tax_rate)
        pf_ta_income.append(next_ta_income)
    vprint(pf_ta_income)

    # calculates reinvestment based on average capex to revenue ratio
    pf_reinvestment = [current_capex]
    for d in pf_revenues[1:]:
        next_reinvestment = d * average_capex_ratio
        pf_reinvestment.append(next_reinvestment)
    vprint(pf_reinvestment)

    # calculates free cash flow to firm
    pf_fcff = [current_cash_flow]
    for e in pf_ta_income[1:]:
        next_fcff = e - pf_reinvestment[len(pf_fcff)]
        pf_fcff.append(next_fcff)
    vprint(pf_fcff)

    # calculates accumulated discount factor
    discount_factor = [1/(1+(wacc(symbol)))]
    for f in range(MODEL_LENGTH):
        next_discount_factor = discount_factor[len(discount_factor)-1] * (1/(1+(wacc(symbol))))
        discount_factor.append(next_discount_factor)
    vprint(discount_factor)

    # calculates accumulated discount factor present value
    accumulated_dcf = []
    dcf_counter = 0
    for g in pf_fcff[1:]:
        next_pv = g * discount_factor[dcf_counter]
        dcf_counter += 1
        accumulated_dcf.append(next_pv)
    vprint(accumulated_dcf)
"""



#if __name__ == "__main__":
#    dcf("AAPL")

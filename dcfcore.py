import os
import sys
PATH_TO_API = os.path.abspath("../FinMesh")
sys.path.insert(0, PATH_TO_API)
import iex.stock
import usgov.yieldcurve
from bs4 import BeautifulSoup as bs
import requests
from scipy import stats
import numpy
import re
from requests_html import HTMLSession
import stockclass

VERBOSE = True

def vprint(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

#DAMODARAN_URL = 'http://pages.stern.nyu.edu/~adamodar/'



def beta(symbol, period=None, method=None, averaging=None, index=None):
    # DEFAULTS
    if not period:
        period = '5y'
    if not averaging:
        averaging = 5
    company_historic = iex.stock.chart(symbol, period=period, chartCloseOnly=True)
    length = len(company_historic)

    # INDEX - Specify index and establish default
    if index:
        index_historic = iex.stock.chart(index, period=period, chartCloseOnly=True)
    else:
        index_historic = iex.stock.chart('SPY', period=period, chartCloseOnly=True)
    assert len(company_historic) == len(index_historic)

    # CLOSE PRICES - Isolating daily close prices
    company_historic_close = []
    index_historic_close = []
    for d in range(len(company_historic)):
        chc = company_historic[d]['close']
        company_historic_close.append(chc)
        ihc = index_historic[d]['close']
        index_historic_close.append(ihc)

    # REGRESSION METHOD - Method is selected with defaults in place
    company_average_close = []
    index_average_close = []
    n = 0 # here n is a counter that will eventually equal length of list
    if method is 'averageReg':
        # AVERAGE REGRESSION - Rolling slice based on Input
        while n + (averaging-1) <= length:
            comp_slice = company_historic_close[n:n + (averaging-1)]
            ind_slice = index_historic_close[n:n + (averaging-1)]
            comp_av = sum(comp_slice)/len(comp_slice)
            ind_av = sum(ind_slice)/len(ind_slice)
            company_average_close.append(comp_av)
            index_average_close.append(ind_av)
            n += 1
        reg = stats.linregress(index_average_close, company_average_close)

    #elif method is 'bottomUpReg':
    #elif method is 'hybridReg':
    else:
        # SIMPLE REGRESSION - Establishes default
        print(company_historic_close)
        reg = stats.linregress(index_historic_close, company_historic_close)

    return reg


# TODO: estimate erp
def erp():
    return 0.40

#
def wacc(symbol, creditRating, income_statement=None, balance_sheet=None, key_stats=None, current_price=None):
    # if this function is nested inside another function with the same requests, pull those instead of making new request
    if not income_statement:
        income_statement = iex.stock.income_statement(symbol, period='annual', last=last_years)
    if not balance_sheet:
        balance_sheet = iex.stock.balance_sheet(symbol, period='annual', last=last_years)
    if not key_stats:
        key_stats = iex.stock.key_stats(symbol)
    if not current_price:
        current_price = iex.stock.price(symbol)
    risk_free = usgov.yieldcurve.get_yield()['10year']
    equity_premium = erp()
    company_beta = beta()
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
    adjusted_debt_risk = ((default_spread + risk_free) * (1 - tax_rate)) * (current_debt / (market_equity + current_debt))
    adjusted_equity_risk = ((equity_premium * beta) + risk_free) * (current_equity / (market_equity + current_debt))
    equity_risk = ((equity_premium * beta) + risk_free)
    debt_risk = (default_spread + risk_free)
    current_wacc = adjusted_debt_risk + adjusted_equity_risk
    return current_wacc

# TODO: estimate terminal wacc
def terminal_wacc():
    return 0.11

def dcf(symbol, creditRating, last_years=None, model_length=None):
    if not last_years:
        last_years = 4
    if not model_length:
        model_length = 5

    # brings in json data from iex finance module
    income_statement = iex.stock.income_statement(symbol, period='annual', last=last_years)
    balance_sheet = iex.stock.balance_sheet(symbol, period='annual', last=last_years)
    cash_flow = iex.stock.cash_flow(symbol, period='annual', last=last_years)
    key_stats = iex.stock.key_stats(symbol)

    # assertains that there are the correct years of data
    assert(len(cash_flow['cashflow']) == last_years) #, "Not enough data")
    assert(len(income_statement['income']) == last_years) #, "Not enough data")
    assert(len(balance_sheet['balancesheet']) == last_years) #, "Not enough data")

    # reference before assignment
    average_revenue_growth = 0
    average_operating_margin = 0
    average_tax_rate = 0
    average_capex_ratio = 0

    # computes averages
    for i in range(last_years-1):
        average_revenue_growth += (income_statement['income'][i]['totalRevenue'] / income_statement['income'][i+1]['totalRevenue']) - 1
        average_operating_margin += income_statement['income'][i]['operatingIncome'] / income_statement['income'][i]['totalRevenue']
        average_tax_rate += income_statement['income'][i]['incomeTax'] / income_statement['income'][i]['pretaxIncome']
        average_capex_ratio += cash_flow['cashflow'][i]['capitalExpenditures'] / income_statement['income'][i]['totalRevenue']
    average_revenue_growth /= last_years - 1
    average_operating_margin /= last_years - 1
    average_tax_rate /= last_years - 1
    average_capex_ratio /= last_years - 1

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

    # calculates pro-forma revenues based on average revenue growth
    # will need to be changed to accept any growth rates
    # NEW FUNCTION that returns a time-series of revenues
    pf_revenues = [current_revenue]
    for a in range(model_length):
        next_revenue = pf_revenues[a] * (1 + average_revenue_growth)
        pf_revenues.append(next_revenue)

    # calculates WACC for the year based on moving to terminal WACC
    wacc_yearly = [wacc(symbol, creditRating)]
    for n in range(model_length):
        next_wacc = wacc_yearly[(len(wacc_yearly)-1)] - ((wacc()-terminal_wacc())/model_length)
        wacc_yearly.append(next_wacc)

    discount_factor = []
    for d in range(model_length):
        if len(discount_factor) == 0:
            next_discount_factor = (1/(1+wacc_yearly[d]))
            discount_factor.append(next_discount_factor)
        else:
            next_discount_factor = discount_factor[(len(discount_factor)-1)] * (1/(1+wacc_yearly[d]))
            discount_factor.append(next_discount_factor)

    # MAIN CALCULATIONS
    # for each year of the model this calculates present value and adds it to a list
    # each of these will need to be changed to allow manipulation of each variable
    yearly_pv = []
    for r in pf_revenues[1:]:
        next_op_marg = r * average_operating_margin
        next_ta_income = next_op_marg * (1-average_tax_rate)
        next_reinvestment = r * average_capex_ratio
        next_fcff = next_ta_income - next_reinvestment
        next_pv = next_fcff * discount_factor[len(yearly_pv)-1]
        yearly_pv.append(next_pv)

    # sums the list of present values
    cumulative_present_value = 0
    for p in yearly_pv:
        cumulative_present_value += p

    # adds/subtracts from cumulative present value
    equity_value = cumulative_present_value + current_cash - current_debt

    # divides by shares outstanding
    value_per_share = equity_value / current_shares_outstanding
    return value_per_share

"""def simple_dcf(symbol, creditRating, analyst=None, compare=None, wacc=None, income_statement=None, key_stats=None, current_price=None, risk_free=None):
    if not income_statement:
        income_statement = iex.stock.income_statement(symbol, period='quarterly', last=1)
    if not cash_flow:
        cash_flow = iex.stock.cash_flow(symbol, period='quarterly', last=1)
    if not key_stats:
        key_stats = iex.stock.key_stats(symbol)
    if not current_price:
        current_price = iex.stock.price(symbol)
    if not wacc:
        wacc = wacc(symbol, creditRating, income_statement=income_statement, current_price=current_price)
    if not risk_free:
            risk_free = usgov.yieldcurve.get_yield()['10year']

    # Simply a PV calculation using the growing perpetuity formula
    current_shares_outstanding = key_stats['sharesOutstanding']
    simple =  ((cash_flow['cashflow'][0]['cashFlow']) / (wacc - risk_free)) / current_shares_outstanding

    if analyst:
        analyst_recc = iex.stock.price_target(symbol)

    if compare:"""

from iexCloud import stock, balanceSheet, cashFlow, company, incomeStatement, keyStats
import usGov.yieldcurve
from scipy import stats

'''
By putting all the data from the requests into an object, it makes it easy to
save and pass around to the functions that need to use the data. TRY NOT TO CHANGE
THIS CLASS! If this class is changed, the saved data will no longer be compatible
'''
class DCF_Data():

    def __init__(self, symbol, last_years=4, index="SPY"):
        self.last = last_years
        self.period = '5y'
        self.symbol = symbol

        self.income_s = incomeStatement.IncomeStatement(self.symbol, period='annual', last=self.last)
        self.balance_s = balanceSheet.BalanceSheet(self.symbol, period='annual', last=self.last)
        self.cash_flow = cashFlow.CashFlow(self.symbol, period='annual', last=self.last)
        self.key_stats = keyStats.KeyStats(self.symbol)


        self.historic_close = stock.chart(self.symbol, period=self.period, chartCloseOnly=True)
        self.price = stock.price(self.symbol)
        self.yield_curve = usGov.yieldcurve.get_yield()

        self.index_historic = stock.chart(index, period=data.period, chartCloseOnly=True)


SPREADS = {
    'aaa': 0.0075, 'aa2': 0.010,  'a1' : 0.0125, 'a2' : 0.0138, 'a3' : 0.0156,
    'baa2' : 0.02, 'ba1' : 0.03,  'ba2' : 0.036, 'b1' : 0.045,  'b2' : 0.054, 'b3' : 0.066,
    'caa' : 0.09,  'ca2' : 0.1108,'c2' : 0.1454,'d2' : 0.1938 }


# TODO: Finish
def beta(data, method='regression', averaging=5):
    length = len(data.historic_close)

    assert len(data.historic_close) == len(self.index_historic)


    company_historic_close = [data.historic_close[i]['close'] for i in range(len(data.historic_close))]
    index_historic_close = [data.index_historic[i]['close'] for i in range(len(data.index_historic))]

    company_average_close = []
    index_average_close = []
    if method is 'averageReg': # AVERAGE REGRESSION - Rolling slice
        for i in range(length - averaging):
            comp_slice = company_historic_close[i:i + (averaging-1)]
            ind_slice = index_historic_close[i:i + (averaging-1)]
            comp_av = sum(comp_slice) / len(comp_slice)
            ind_av = sum(ind_slice) / len(ind_slice)
            company_average_close.append(comp_av)
            index_average_close.append(ind_av)
        reg = stats.linregress(index_average_close, company_average_close)

    elif method is 'bottomUpReg':
        raise ImplementationError("bottomUpReg")

    elif method is 'hybridReg':
        raise ImplementationError("hybridReg")

    elif method is 'regression': # SIMPLE REGRESSION
        reg = stats.linregress(index_historic_close, company_historic_close)
    return reg


# TODO: Finish
def erp():
    return 0.40


# TODO: Finish
def wacc(data, credit_rating):
    risk_free = data.yield_curve['10year']
    equity_premium = erp()
    company_beta = beta(data)

    default_spread = SPREADS[credit_rating]
    tax_rate = data.income_s.raw['income'][0]['incomeTax'] / data.income_s.raw['income'][0]['pretaxIncome']
    current_debt = data.balance_s.raw['balancesheet'][0]['longTermDebt']
    current_shares_outstanding = data.key_stats.raw['sharesOutstanding']
    market_equity = current_shares_outstanding * data.price
    adjusted_debt_risk = ((default_spread + risk_free) * (1 - tax_rate)) * (current_debt / (market_equity + current_debt))
    adjusted_equity_risk = ((equity_premium * company_beta) + risk_free) * (current_equity / (market_equity + current_debt))
    current_wacc = adjusted_debt_risk + adjusted_equity_risk
    return current_wacc


def get_avg_capex_ratio(data):
    acr = 0
    for i in range(data.last-1):
        acr += data.cash_flow.raw['cashflow'][i]['capitalExpenditures'] / data.income_s.raw['income'][i]['totalRevenue']
    return acr


def get_pf_revenues(data, avg_revenue_growth, model_len):
    pf_revenues = [data.income_s.raw['income'][0]['totalRevenue']]
    for a in range(model_len):
        next_revenue = pf_revenues[a] * (1 + avg_revenue_growth)
        pf_revenues.append(next_revenue)
    return pf_revenues


# TODO: estimate terminal wacc
def terminal_wacc():
    return 0.11


def get_wacc_yearly(data, model_len, credit_rating):
    wacc_yearly = [wacc(data, credit_rating)]
    for n in range(model_len):
        next_wacc = wacc_yearly[(len(wacc_yearly)-1)] - ((wacc(data, credit_rating) - terminal_wacc())/model_len)
        wacc_yearly.append(next_wacc)
    return wacc_yearly


def get_discount_factor(data, model_len, credit_rating):
    wacc_yearly = get_wacc_yearly(data, model_len, credit_rating)
    df = [(1/(1+wacc_yearly[d]))]
    for d in range(1, model_len):
        n_df = df[(len(df)-1)] * (1/(1+wacc_yearly[d]))
        df.append(n_df)


def compute_dcf(data : DCF_Data, credit_rating, model_len = 5):
    avg_revenue_growth = data.income_s.get_avg_revenue_growth()
    avg_tax_rate = data.income_s.get_avg_tax_rate()
    avg_operating_margin = data.income_s.get_avg_operating_margin()
    avg_capex_ratio = get_avg_capex_ratio(data)

    # current values for 'base year'
    curr_revenue = data.income_s.raw['income'][0]['totalRevenue']
    curr_operating_income = data.income_s.raw['income'][0]['operatingIncome']
    curr_tax_paid = data.income_s.raw['income'][0]['incomeTax']
    curr_tax_adjusted_income = curr_operating_income - curr_tax_paid
    curr_capex = data.cash_flow.raw['cashflow'][0]['capitalExpenditures']
    curr_cash_flow = data.cash_flow.raw['cashflow'][0]['cashFlow']
    curr_operating_margin = curr_operating_income / curr_revenue
    curr_debt = data.balance_s.raw['balancesheet'][0]['longTermDebt']
    curr_cash = (data.balance_s.raw['balancesheet'][0]['currentCash'] + data.balance_s.raw['balancesheet'][0]['shortTermInvestments'])
    curr_shares_outstanding = data.key_stats.raw['sharesOutstanding']


    pf_revenues = get_pf_revenues(data, avg_revenue_growth, model_len)
    discount_factor = get_discount_factor(data, model_len, credit_rating)

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

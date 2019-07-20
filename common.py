import os
import sys
PATH_TO_API = os.path.abspath("../FinMesh")
sys.path.insert(0, PATH_TO_API)
import iex.stock
import usgov.yieldcurve

#Nothing

# Takes a list of values and finds the growth rate
def growth_rate(values, growthType):
    # returns basic averages
    if growthType == basic:
        position = 0
        list_of_growth_rates = []
        for value in values[1:]:
            list_of_growth_rates.append((value-values[position])/values[position])
            position += 1
        result = average(list_of_growth_rates)

    # returns CAGR
    if growthType == cagr:
        result = (values[len(list-1)]-values[0]/values[0])/len(values)

    else:
        result = 'Please enter valid growth type.'

    return result

# Takes a list of values and finds the simple moving average of them
def moving_average(list):
    # returns new list with moving average
    pass

# Takes financial information and returns the most recent data available
def last_reported(json):
    # returns most recent value or string
    # used in building base year financials and for fetching the actual date of reporting
    pass

# Takes a static growth rate and a base value and builds x number of years of financial data
def static_proforma_build(growth, base, years):
    counter = 0
    proforma_values = []
    while counter <= years:
        if counter == 0:
            proforma_values.append(base * growth)
        else:
            proforma_values.append(proforma_values[counter-1] * growth)
    return proforma_values

# Takes a list of premade ratios or rates (y) and finds the pro-forma values for x
def dynamic_proforma_build(ratio, list_y, base_x):
    #returns new list conforming to ratio or rate
    pass

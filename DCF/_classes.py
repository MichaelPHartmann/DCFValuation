class forecast(object):
    ## All forecasting objects share certain operations. Included are uniform, incdec, and specific

    def __init__(self):
        pass

    def uniform(self, base, growth, length):
        ## Returns forecasted values based on uniform growth.
        assert isinstance(growth, float), "You must enter an integer or float!"
        fc_values = [base]
        for n in range(length):
            next_value = fc_values[n]*(1+growth)
            fc_values.append(next_value)
        fc_values.pop(0)
        return fc_values

    def incdec(self, base, start, end, length):
        ## Returns forecasted values based on an increasing or decreasing growth.
        assert isinstance(start, float) and isinstance(end, float), "You must enter an integer or float!"
        increment = (float(end)-float(start))/(length-1)
        fc_values = [base]
        growth_rates = [start]
        for n in range(length-1):
            next_rate = growth_rates[n] + increment
            growth_rates.append(next_rate)
        for r in range(length):
            next_value = fc_values[r] * (1+growth_rates[r])
            fc_values.append(next_value)
        fc_values.pop(0)
        return fc_values

    def specific(self, base, values, length):
        ## Returns forecasted values based on the specific growth rates entered.
        assert isinstance(values, list), "You must enter a list!"
        fc_values = [base]
        list_length = len(values)
        assert list_length == length , f'Number of values in list ({list_length}) must be same as length parameter ({length})!'
        for r in range(length):
            next_value = fc_values[r]*(1+values[r])
            fc_values.append(next_value)
        fc_values.pop(0)
        return fc_values

class Average():
    ## All averaging objects share certain operations. Included are straight average and annualized.

    def __init__(self):
        pass

    def average(values):
        years_of_data = len(values)
        change = []
        for n in range(years_of_data-1):
            percent_change_yearly = (series[n+1]-series[n])/series[n]
            change.append(percent_change)
        result = (sum(change)/years_of_data)
        return result

    def annualized(values):
        years_of_data = len(values)
        result = ((series[years_of_data-1]-series[0])/series[0])/years_of_data
        return result


"""
def forecast_revenue(base, method='uniform', length=5, growth=None, start=None, end=None, specific_rates=None):

    if method is 'uniform':
        assert growth != None, 'You must enter a value in the base_growth parameter!'
        forecast_instantiation = forecast()
        result = forecast_instantiation.uniform(base, growth, length)

    if method is 'incdec':
        assert start != None, 'You must enter a value to the start parameter!'
        assert end != None, 'You must enter a value to end parameter!'
        forecast_instantiation = forecast()
        result = forecast_instantiation.incdec(base, start, end, length)

    if method is 'specific':
        list_length = len(specific_rates)
        assert list_length == length , f'Number of values in list ({list_length}) must be same as length parameter ({length})!'
        forecast_instantiation = forecast()
        result = forecast_instantiation(base, specific_rates, length)

    else:
        result = 'Please enter a valid method!'

    return result
"""

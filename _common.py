
#  ____                                    ____                   _   _
# |  _ \ _____   _____ _ __  _   _  ___   / ___|_ __ _____      _| |_| |__
# | |_) / _ \ \ / / _ \ '_ \| | | |/ _ \ | |  _| '__/ _ \ \ /\ / / __| '_ \
# |  _ <  __/\ V /  __/ | | | |_| |  __/ | |_| | | | (_) \ V  V /| |_| | | |
# |_| \_\___| \_/ \___|_| |_|\__,_|\___|  \____|_|  \___/ \_/\_/  \__|_| |_|

def historical_growth(series, method='annualized'):
    years_of_data = len(series)
    change = []
    # Returns the average growth of each individual year.
    if method is 'average' or None:
        for n in range(years_of_data-1):
            percent_change_yearly = (series[n+1]-series[n])/series[n]
            change.append(percent_change)
        return (sum(change)/years_of_data)
    # Returns annualized growth.
    if method is 'annualized':
        annualized_change = ((series[years_of_data-1]-series[0])/series[0])/years_of_data
        return annualized_change

def forecasted_growth(base_value, length=5, method='incdec', base_growth=None, direction=None, start=0.025, end=0.05, specific_rates=None):
    fc_revenue = [base_value]
    # Returns forecasted revenue based on a uniform revenue growth
    if method is 'uniform':
        assert base_growth != None, 'You must enter a value in the base_growth parameter!'
        for n in range(length):
            next_value = fc_revenue[n]*base_growth
            fc_revenue.append(next_value)
        fc_revenue.pop(0)
    # Returns forecasted revenue based on an increasing or decreasing revenue growth.
    if method is 'incdec':
        assert start != None, 'You must enter a value to the start parameter!'
        assert end != None, 'You must enter a value to end parameter!'
        increment = (float(end)-float(start))/(length-1)
        growth_rates = [start]
        for n in range(length-1):
            next_rate = growth_rates[n]+increment
            growth_rates.append(next_rate)
        for r in range(length):
            next_value = fc_revenue[r]*(1+growth_rates[r])
            fc_revenue.append(next_value)
        fc_revenue.pop(0)
    # Returns forecasted revenue based on the specific growth rates entered.
    if method is 'specific':
        list_length = len(specific_rates)
        assert list_length == length , f'Number of values in list ({list_length}) must be same as length parameter ({length})!'
        for r in range(length):
            next_value = fc_revenue[r]*(1+specific_rates[r])
            fc_revenue.append(next_value)
        fc_revenue.pop(0)
    return fc_revenue

#  __  __                 _          ____      _            _       _   _
# |  \/  | __ _ _ __ __ _(_)_ __    / ___|__ _| | ___ _   _| | __ _| |_(_) ___  _ __
# | |\/| |/ _` | '__/ _` | | '_ \  | |   / _` | |/ __| | | | |/ _` | __| |/ _ \| '_ \
# | |  | | (_| | | | (_| | | | | | | |__| (_| | | (__| |_| | | (_| | |_| | (_) | | | |
# |_|  |_|\__,_|_|  \__, |_|_| |_|  \____\__,_|_|\___|\__,_|_|\__,_|\__|_|\___/|_| |_|
#                   |___/


#  ____      _                     _                        _
# |  _ \ ___(_)_ ____   _____  ___| |_ _ __ ___   ___ _ __ | |_
# | |_) / _ \ | '_ \ \ / / _ \/ __| __| '_ ` _ \ / _ \ '_ \| __|
# |  _ <  __/ | | | \ V /  __/\__ \ |_| | | | | |  __/ | | | |_
# |_| \_\___|_|_| |_|\_/ \___||___/\__|_| |_| |_|\___|_| |_|\__|


#  ____       _
# | __ )  ___| |_ __ _
# |  _ \ / _ \ __/ _` |
# | |_) |  __/ || (_| |
# |____/ \___|\__\__,_|


#   ____          _            __    ____            _ _        _
#  / ___|___  ___| |_    ___  / _|  / ___|__ _ _ __ (_) |_ __ _| |
# | |   / _ \/ __| __|  / _ \| |_  | |   / _` | '_ \| | __/ _` | |
# | |__| (_) \__ \ |_  | (_) |  _| | |__| (_| | |_) | | || (_| | |
#  \____\___/|___/\__|  \___/|_|    \____\__,_| .__/|_|\__\__,_|_|
#                                             |_|

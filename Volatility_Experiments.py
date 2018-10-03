import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from Instrument import Straddle
from dataUlt import (import_yahoo_data, daily_ret,
    daily_to_monthly_ret)

# (b)
# before you run, edit import_yahoo_data() path
SPY = import_yahoo_data('SPY.csv')
VIX_daily = import_yahoo_data('^VIX_daily.csv')['Adj Close'] / 100
VIX_monthly = import_yahoo_data('^VIX_monthly.csv')['Adj Close'] / 100
SPY_daily_ret = daily_ret(SPY)
print("The autocorrelation of SPY is: ", 
    SPY_daily_ret.autocorr(lag=1),'\n', 
    "The autocorrelation of VIX is: ", 
    VIX_daily.autocorr(lag=1),'\n',
    "I fould strong evidence of autocorrelation in VIX.\n",
    "I would expect VIX to be more autocorrelated.\n")

# (c)
matrix_daily = pd.concat([SPY_daily_ret, VIX_daily],
    axis=1, keys=['SPY', 'VIX'])
matrix_daily.dropna(how='any', axis=0, inplace=True)


SPY_monthly_ret = daily_to_monthly_ret(SPY_daily_ret)
VIX_monthly = VIX_monthly.groupby([VIX_monthly.index.year, VIX_monthly.index.month]).first()
matrix_monthly = pd.concat([SPY_monthly_ret, VIX_monthly], axis=1, keys=['SPY', 'VIX'])
matrix_monthly.dropna(how='any', axis=0, inplace=True)

corr_daily= matrix_daily.corr()
corr_montly = matrix_monthly.corr()
print("correlation on a daily base is: \n",corr_daily,'\n',
    "correlation on a monthly base is: \n",corr_montly,'\n',
    "the correlation is signicantly negative.\n",
    "the implication is: the assumption of BS model",
    "that the volatility is constant doesn't hold,",
    "as the price of underlying asset is moving.\n")

# (d)
corr_roll = matrix_daily.rolling(window=90).corr()
corr_roll = corr_roll.ix[corr_roll.index.get_level_values(1) == 'SPY']
corr_roll.dropna(axis=0, how='any', inplace=True)
corr_roll.drop(columns='SPY', inplace=True)
corr_roll.index = corr_roll.index.droplevel(level=1)
corr_roll.rename(columns={'VIX':'SPY_VIX'})
corr_roll.plot(title='90-day correlatons of SPY and VIX',legend=False)
plt.show()
print("As it's shown in the picture,",
    "correlation deviate the most from long-run average in year 2018")

# (e)
real_std_roll = SPY_daily_ret.rolling(window=90).std() * np.sqrt(252)
matrix_std_roll = pd.concat([real_std_roll, VIX_daily], axis=1, keys=['Real', 'Imply'])
matrix_std_roll.dropna(how='any', axis=0, inplace=True)
matrix_std_roll['Premium'] = matrix_std_roll['Imply'] -  matrix_std_roll['Real']
matrix_std_roll['Premium'].plot(title='Premium of implied vol. over realized vol.')
plt.show()

# (f) and (g)
straddle_price = pd.Series(index=matrix_daily.index)
straddle_payoff = pd.Series(index=matrix_daily.index)
for i in range(len(matrix_daily)):
    s0 = SPY.ix[i,'Adj Close']
    sigma = matrix_daily.ix[i,'VIX']
    Straddle_a = Straddle(k1 = s0, k2 = s0, pos='long')
    straddle_price.iloc[i] = Straddle_a.price_bs(s0=s0, r=0, sigma=sigma, T=1.0/12)
    if i <= len(matrix_daily)-20:
        straddle_payoff.iloc[i] = Straddle_a.payoff(SPY.ix[i+20,'Adj Close'])
profit_loss = straddle_payoff - straddle_price
print("the average of P&L is: ", profit_loss.mean(), '\n')
straddle_price.plot(title='Price of straddle by BS model')
plt.show()
straddle_payoff.plot(title='Payoff of straddle')
plt.show()
profit_loss.plot(title='P&L')
plt.show()

profit_loss.to_csv('P&L.csv')
# (h)
matrix_scatter = pd.concat([profit_loss, matrix_std_roll['Premium']], axis=1, keys=['P&L', 'Premium'])
matrix_scatter.dropna(how='any', axis=0, inplace=True)
matrix_scatter.plot.scatter(title='P&L against Premium', x = 'Premium', y = 'P&L')
plt.show()


pass 
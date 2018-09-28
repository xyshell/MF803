import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

from dataUlt import import_yahoo_data, daily_ret, daily_to_monthly_ret

# (b)
# before you run, edit import_yahoo_data() path
SPY = import_yahoo_data('SPY.csv')
VIX = import_yahoo_data('^VIX.csv')['Adj Close']
SPY_daily_ret = daily_ret(SPY)
print("The autocorrelation of SPY is: ", 
    SPY_daily_ret.autocorr(lag=1),'\n', 
    "The autocorrelation of VIX is: ", 
    VIX.autocorr(lag=1),'\n',
    "I fould strong evidence of autocorrelation in VIX.\n",
    "I would expect VIX to be more autocorrelated.\n")

# TODO 
# (c)
matrix_daily_ret = pd.concat([SPY_daily_ret, VIX],
    axis=1, keys=['SPY', 'VIX'])
SPY_monthly_ret = daily_to_monthly_ret(SPY_daily_ret)
VIX_monthly_ret = daily_to_monthly_ret(VIX)
matrix_monthly_ret = pd.concat([SPY_monthly_ret, VIX_monthly_ret],
    axis=1, keys=['SPY', 'VIX'])
corr_matrix_daily_ret = matrix_daily_ret.corr()
corr_matrix_montly_ret = matrix_monthly_ret.corr()
print("correlation on a daily base is: \n",corr_matrix_daily_ret,'\n',
    "correlation on a monthly base is: \n",corr_matrix_montly_ret,'\n',
    "the correlation is signicantly negative.\n",
    "the implication is: the assumption of BS model",
    "that the volatility is constant doesn't hold,",
    "as the price of underlying asset is moving.\n")

# (d)
corr_roll = matrix_daily_ret.rolling(window=90).corr()
corr_roll = corr_roll.ix[corr_roll.index.get_level_values(1) == 'SPY']
corr_roll.dropna(axis=0, how='any', inplace=True)
corr_roll.drop(columns='SPY', inplace=True)
corr_roll.index = corr_roll.index.droplevel(level=1)
corr_roll.rename(columns={'VIX':'SPY_VIX'})
corr_roll.plot(title='90-day correlatons of SPY and VIX',legend=False)
# plt.show()
print("As it's shown in the picture,",
    "correlation deviate the most from long-run average in year 2012")

# (e)
real_std_roll = SPY_daily_ret.rolling(window=90).std()
real_std_roll.to_csv("real_std_roll.csv")
imply_std_roll = VIX.rolling(window=90).std()
imply_std_roll.to_csv("imply_std_roll.csv")

    
pass 
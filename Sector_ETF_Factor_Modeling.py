import platform
import numpy as np
import pandas as pd
from statsmodels.graphics.gofplots import qqplot
from sklearn.linear_model import LinearRegression
from dataUlt import import_fama_data, ETF_dict

# (a)
if platform.system() == 'Darwin':
    path = '/Users/xieyou/GitHub/MF803'
else:
    path = 'C:\\Users\\47494\\GitHub\\MF803'

three_factors = import_fama_data(path, 'Fama_French_Three_Factors_Daily')

# (b)
three_factors_cov = three_factors.cov()
three_factors_corr = three_factors.corr()
print(three_factors_corr)
print('These factors are not correlated')

if platform.system() == 'Darwin':
    ETF_corr = pd.read_csv(path + '/result/ ' +'ETFs_corr_daily.csv')
else:
    ETF_corr = pd.read_csv(path + '\\result\\ ' +'ETFs_corr_daily.csv')

# (c)
three_factors_corr_roll = three_factors.rolling(window=90).corr()
if platform.system() == 'Darwin':
    ETF_corr_roll = pd.read_csv(path + '/result/ ' +'corr_roll.csv')
else:
    ETF_corr_roll = pd.read_csv(path + '\\result\\ ' +'corr_roll.csv')

# (d)
qqplot(np.array(three_factors['mkt'].values))
qqplot(np.array(three_factors['smb'].values))
qqplot(np.array(three_factors['hml'].values))

# (e)
linreg = LinearRegression()
beta = {}
for Ticker in ETF_dict.keys():
    exec("linreg.fit(SPY_daily_ret.values.reshape(-1,1)," +
            Ticker+"_daily_ret.values.reshape(-1,1))")
    beta[Ticker] = float(linreg.coef_)

beta_roll = pd.DataFrame()
for Ticker in ETF_dict.keys():
    for i in range(89, len(SPY_daily_ret), 1):
        SPY_window = SPY_daily_ret.iloc[i-89:i]
        exec(Ticker+"_window = "+Ticker+"_daily_ret.iloc[i-89:i]")
        exec("linreg.fit(SPY_window.values.reshape(-1,1)," +
                Ticker+"_window.values.reshape(-1,1))")
        beta_roll.ix[i-89, Ticker] = float(linreg.coef_)

# (f)
return_real = None
return_pred = None
residual = return_real - return_pred
print('mean of residual is: ', np.mean(residual), '\n')
print('variance of residual is: ', np.var(residual), '\n')
qqplot((residual.values))

# Autocorrelation, Heteroscedastic
import platform
import numpy as np
import pandas as pd
from statsmodels.graphics.gofplots import qqplot
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from dataUlt import import_fama_data, get_result, ETF_DICT

# (a)
three_factors = import_fama_data(
    'Fama_French_Three_Factors_Daily.csv')
del three_factors['RF']

# (b)
three_factors_cov = three_factors.cov()
three_factors_corr = three_factors.corr()
print(three_factors_corr)
print('These factors are not correlated')
ETF_corr = get_result('ETF_daily_corr.csv')
print('By comparing to the correlation of ETFs, '+
    'These factors are less correlated')

# (c)
three_factors_corr_roll = three_factors.rolling(window=90).corr()
three_factors_corr_roll.dropna(axis=0, how='any', inplace=True)
loc1 = three_factors_corr_roll.index.get_level_values(1) == 'Mkt-RF'
df1 = three_factors_corr_roll[loc1][['SMB']] # Mkt-RF and SMB
df2 = three_factors_corr_roll[loc1][['HML']] # Mkt-RF and HML
loc2 = three_factors_corr_roll.index.get_level_values(1) == 'SMB'
df3 = three_factors_corr_roll[loc2][['HML']] # SMB and HML

three_factors_corr_roll = pd.DataFrame(
    data=np.hstack((df1.values,df2.values,df3.values)),
    index=df1.index.droplevel(level=1),
    columns=['Mkt-RF and SMB', 'Mkt-RF and HML', 'SMB and HML'])

ETF_corr_roll = get_result('ETF_daily_corr_roll.csv')
print("the three_factors_corr_roll is not stable over time.\n" +
    "there's no evidence that they are more stable than ETF.\n")

# (d)
fig = plt.figure(figsize=(20,5))
fig.suptitle('Qqplot Normal Test',fontsize=15)
ax1 = plt.subplot(131)
ax1.set_title('Mkt-RF')
qqplot(three_factors['Mkt-RF'].values, ax=ax1)
ax2 = plt.subplot(132)
ax2.set_title('SMB')
qqplot(three_factors['SMB'].values, ax=ax2)
ax3 = plt.subplot(133)
ax3.set_title('HML')
qqplot(three_factors['HML'].values, ax=ax3)
plt.show()

# (e)
ETF_ret = get_result('ETF_daily_ret.csv')
ETF_ret['Date'] = pd.to_datetime(ETF_ret['Date'])
ETF_ret.set_index('Date', inplace=True)
fama_model = ETF_ret.merge(three_factors,
    left_index=True, right_index=True)

linreg0 = LinearRegression()
linreg0.fit(fama_model[['Mkt-RF','SMB','HML']].values,
    fama_model[[i for i in ETF_DICT.keys()]].values)
beta = dict(zip(ETF_DICT.keys(), linreg0.coef_[:,0]))
print("beta for the entire historical period is: \n", beta)

linreg1 = LinearRegression()
beta_roll = pd.DataFrame()
for i in range(89, len(fama_model), 1):
    fama_model_window = fama_model.iloc[i-89:i]
    linreg1.fit(fama_model_window[['Mkt-RF','SMB','HML']].values,
        fama_model_window[[x for x in ETF_DICT.keys()]].values)
    beta_temp = pd.DataFrame(linreg1.coef_[:,0].reshape(-1,10), 
        columns = [x for x in ETF_DICT.keys()], 
        index = [fama_model_window.index[-1]])
    beta_roll = pd.concat([beta_roll, beta_temp])
print("these's little evidence showing beta gets more consistant,"+ 
    "while it somewhat gets more 'compact'")

# (f)
for i in range(len(ETF_DICT)):
for i in range(len(ETF_dict)):
    pred_ret = (linreg0.coef_[i] * 
        fama_model[['Mkt-RF','SMB','HML']]).sum(axis=1)
    real_ret = fama_model.iloc[:,i]
    residual[list(ETF_DICT.keys())[i]] = residual_temp
    residual[list(ETF_dict.keys())[i]] = residual_temp
print("mean of residual is: \n",residual.mean(axis=0),'\n')
print("var of residual is: \n",residual.var(axis=0),'\n')

for i in range(len(ETF_DICT)-1):
for i in range(len(ETF_dict)-1):
    exec("ax"+str(i+1)+" = plt.subplot(33"+str(i+1)+")")
    exec("ax"+str(i+1)+".set_title(list(ETF_dict.keys())["+
        str(i)+"])")
    exec("qqplot(residual[list(ETF_dict.keys())["+
        str(i)+"]].values, ax=ax"+str(i+1)+")")
plt.show()

print("the residual appears to be normal, which supports the model"+
    "at some extent.\nAlso, one could test whether residual is"+
    "auto-correlated.\nThe auto-correlation of the residual is:\n")

for i in range(len(ETF_dict)):
for i in range(len(ETF_DICT)):
    print(list(ETF_DICT.keys())[i],' : ',
print("\nexcept for SPY, the result supports the assumption of OLS.")
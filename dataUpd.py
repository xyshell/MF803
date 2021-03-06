import pandas as pd
from dataUlt import *

# read data
for Ticker in ETF_DICT.keys():
    exec(Ticker+" = import_yahoo_data('"+Ticker+".csv')")

# update ETF_daily_ret, ETF_monthly_ret
for Ticker in ETF_DICT.keys():
    exec(Ticker+"_daily_ret = daily_ret("+Ticker+").dropna(how='any')")
    exec(Ticker+"_monthly_ret = daily_to_monthly_ret("+Ticker+"_daily_ret)")
matrix_daily_ret = None
matrix_monthly_ret = None
exec("matrix_daily_ret = pd.concat("+str([Ticker+"_daily_ret" for Ticker in ETF_DICT.keys(
)]).replace("'", "")+", axis=1, keys="+str([Ticker for Ticker in ETF_DICT.keys()])+")")
exec("matrix_monthly_ret = pd.concat("+str([Ticker+"_monthly_ret" for Ticker in ETF_DICT.keys(
)]).replace("'", "")+", axis=1, keys="+str([Ticker for Ticker in ETF_DICT.keys()])+")")
matrix_daily_ret.to_csv(result_path + 'ETFs_daily_ret.csv')
matrix_monthly_ret.to_csv(result_path + 'ETFs_monthly_ret.csv')

# update ETF_daily_cov, ETF_daily_corr
cov_matrix_daily_ret = matrix_daily_ret.cov()
cov_matrix_monthly_ret = matrix_monthly_ret.cov()
corr_matrix_daily_ret = matrix_daily_ret.corr()
corr_matrix_monthly_ret = matrix_monthly_ret.corr()
cov_matrix_daily_ret.to_csv(result_path + 'ETFs_daily_cov.csv')
cov_matrix_monthly_ret.to_csv(result_path + 'ETFs_monthly_cov.csv')
corr_matrix_daily_ret.to_csv(result_path + 'ETFs_daily_corr.csv')
corr_matrix_monthly_ret.to_csv(result_path + 'ETFs_monthly_corr.csv')



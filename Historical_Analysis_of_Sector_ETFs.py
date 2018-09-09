import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

datapath = 'C:\\Users\\47494\\GitHub\\MF803\\data'


def import_yahoo_data(filename):
    '''input filename(ex.SPY), output dataframe with date index'''
    filepath = datapath + '\\' + filename + '.csv'
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df


def daily_ret(df):
    '''input df, output series of daily log return'''
    return np.log(df['Adj Close'] / df['Adj Close'].shift(-1))


def daily_to_monthly_ret(df):
    '''input df, output series of monthly log return'''
    return df.groupby([df.index.year, df.index.month]).sum()


def annual_ret_std(df):
    ''' input df, output annulized return and std'''
    logret = daily_ret(df)
    annual_ret = np.nansum(logret.values)
    annual_std = np.nanstd(logret.values) * 252 ** 0.5
    return annual_ret, annual_std


if __name__ == '__main__':
    ETF_dict = {'SPY': 'S&P Index',
                'XLB': 'Materials',
                'XLE': 'Energy',
                'XLF': 'Financials',
                'XLI': 'Industrials',
                'XLK': 'Technology',
                'XLP': 'Consumer Staples',
                'XLU': 'Utilities',
                'XLV': 'Healthcare',
                'XLY': 'Consumer Discretionary'}

    '''read data'''
    for Ticker in ETF_dict.keys():
        exec(Ticker+" = import_yahoo_data('"+Ticker+"')")

    '''Calculate the annualized return and standard deviation of each ETF'''
    for Ticker in ETF_dict.keys():
        exec(Ticker+"_ret, "+Ticker+"_std" + " = annual_ret_std("+Ticker+")")

    '''Calculate the covariance matrix of daily and monthly returns. Comment on difference of the two'''
    for Ticker in ETF_dict.keys():
        exec(Ticker+"_daily_ret = daily_ret("+Ticker+")")
        exec(Ticker+"_monthly_ret = daily_to_monthly_ret("+Ticker+"_daily_ret)")
    
    matrix_daily_ret = pd.DataFrame()
    matrix_monthly_ret = pd.DataFrame()
    exec("matrix_daily_ret = pd.concat("+str([Ticker+"_daily_ret" for Ticker in ETF_dict.keys()]).replace("'","")+", axis=1, keys="+str([Ticker for Ticker in ETF_dict.keys()])+")")
    exec("matrix_monthly_ret = pd.concat("+str([Ticker+"_monthly_ret" for Ticker in ETF_dict.keys()]).replace("'","")+", axis=1, keys="+str([Ticker for Ticker in ETF_dict.keys()])+")")
    cov_matrix_daily_ret = matrix_daily_ret.cov()
    cov_matrix_monthly_ret = matrix_monthly_ret.cov()

    ticks = np.arange(0,len(ETF_dict),1)
    names = list(ETF_dict.keys())
    fig = plt.figure(figsize=(14,5))

    ax = fig.add_subplot(121)
    cax = ax.matshow(cov_matrix_daily_ret, vmin=cov_matrix_daily_ret.min().min(), vmax=cov_matrix_daily_ret.max().max())  #绘制热力图，从-1到1
    fig.colorbar(cax)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(names)
    ax.set_yticklabels(names)

    bx = fig.add_subplot(122)
    cbx = bx.matshow(cov_matrix_monthly_ret, vmin=cov_matrix_monthly_ret.min().min(), vmax=cov_matrix_monthly_ret.max().max())  #绘制热力图，从-1到1
    fig.colorbar(cbx)
    bx.set_xticks(ticks)
    bx.set_yticks(ticks)
    bx.set_xticklabels(names)
    bx.set_yticklabels(names)
    plt.show()
    # the covs of daily returns and monthly returns vary for absolute value, 
    # while they remain similar after being scaled.

    '''Calculate a rolling 90-day correlation of each sector ETF with the S&P index.'''
    roll_corr = matrix_daily_ret.rolling(window=90).corr()
    roll_corr = roll_corr.ix[roll_corr.index.get_level_values(1) == 'SPY']
    roll_corr.dropna(axis=0, how='any', inplace=True)
    roll_corr.drop(columns='SPY',inplace=True)
    roll_corr.index = roll_corr.index.droplevel(level=1)
    roll_corr.plot()
    plt.show()
    # the correlations are not stable over time
    # I think the S&P's fluctuations cause them vary

    x = 1

    # roll_corr.to_csv('roll_corr.csv')
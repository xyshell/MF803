import platform
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def import_yahoo_data(datapath, filename):
    '''input filename(ex.SPY), output dataframe with date index'''
    filepath = datapath + filename + '.csv'
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df


def daily_ret(df):
    '''input df, output series of daily log return'''
    return np.log(df['Adj Close'] / df['Adj Close'].shift(1))


def daily_to_monthly_ret(df):
    '''input df, output series of monthly log return'''
    return df.groupby([df.index.year, df.index.month]).sum()


def annual_ret_std(df):
    ''' input df, output annulized return and std'''
    logret = daily_ret(df)
    annual_ret = np.nansum(logret.values / len(logret) * 252)
    annual_std = np.nanstd(logret.values) * 252 ** 0.5
    return annual_ret, annual_std


if __name__ == '__main__':
    
    if platform.system() == 'Darwin':
        datapath = '/Users/xieyou/GitHub/MF803/data/'
    else:
        datapath = 'C:\\Users\\47494\\GitHub\\MF803\\data\\'
    
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
        exec(Ticker+" = import_yahoo_data(datapath, '"+Ticker+"')")
    print("data has been downloaded to file 'data'\n")

    '''Calculate the annualized return and standard deviation of ETFs'''
    for Ticker in ETF_dict.keys():
        exec(Ticker+"_ret, "+Ticker+"_std" + " = annual_ret_std("+Ticker+")")
    print("annualized return and standard deviation are saved in" +
          " 'Ticker_ret' and 'Ticker_std' \n")

    '''Calculate the covariance matrix of daily and monthly returns.'''
    for Ticker in ETF_dict.keys():
        exec(Ticker+"_daily_ret = daily_ret("+Ticker+").dropna(how='any')")
        exec(Ticker+"_monthly_ret = daily_to_monthly_ret("+Ticker+"_daily_ret)")

    matrix_daily_ret = pd.DataFrame()
    matrix_monthly_ret = pd.DataFrame()
    exec("matrix_daily_ret = pd.concat("+str([Ticker+"_daily_ret" for Ticker in ETF_dict.keys(
    )]).replace("'", "")+", axis=1, keys="+str([Ticker for Ticker in ETF_dict.keys()])+")")
    exec("matrix_monthly_ret = pd.concat("+str([Ticker+"_monthly_ret" for Ticker in ETF_dict.keys(
    )]).replace("'", "")+", axis=1, keys="+str([Ticker for Ticker in ETF_dict.keys()])+")")
    cov_matrix_daily_ret = matrix_daily_ret.cov()
    cov_matrix_monthly_ret = matrix_monthly_ret.cov()
    corr_matrix_daily_ret = matrix_daily_ret.corr()
    corr_matrix_monthly_ret = matrix_monthly_ret.corr()

    ticks = np.arange(0, len(ETF_dict), 1)
    names = list(ETF_dict.keys())
    fig = plt.figure(figsize=(14, 5))

    ax = fig.add_subplot(121)
    cax = ax.matshow(corr_matrix_daily_ret, vmin=corr_matrix_daily_ret.min(
    ).min(), vmax=corr_matrix_daily_ret.max().max())
    fig.colorbar(cax)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(names)
    ax.set_yticklabels(names)

    bx = fig.add_subplot(122)
    cbx = bx.matshow(corr_matrix_monthly_ret, vmin=corr_matrix_monthly_ret.min(
    ).min(), vmax=corr_matrix_monthly_ret.max().max())
    fig.colorbar(cbx)
    bx.set_xticks(ticks)
    bx.set_yticks(ticks)
    bx.set_xticklabels(names)
    bx.set_yticklabels(names)
    plt.show()
    print("covariance matrix of daily returns are saved in 'cov_matrix_daily_ret'" +
          " and that of monthly returns are saved in 'cov_matrix_monthly_ret'," +
          " picture has been drawn for visulization\n")
    # the covs of daily returns and monthly returns vary for absolute value,
    # while they remain similar after being scaled.

    '''Calculate a rolling 90-day correlation of each sector ETF with the S&P index.'''
    corr_roll = matrix_daily_ret.rolling(window=90).corr()
    corr_roll = corr_roll.ix[corr_roll.index.get_level_values(1) == 'SPY']
    corr_roll.dropna(axis=0, how='any', inplace=True)
    corr_roll.drop(columns='SPY', inplace=True)
    corr_roll.index = corr_roll.index.droplevel(level=1)
    corr_roll.plot()
    plt.show()
    corr_roll.to_csv('corr_roll.csv')
    print("90-day rolling correlation is saved in 'corr_roll'\n")
    # the correlations are not stable over time
    # I think the S&P's fluctuations cause them vary

    '''For each sector ETF, compute it's 
 to the market using the CAPM model
       Compute the 
 for the entire historical period and also rolling 90-day's'''
    linreg = LinearRegression()
    beta = {}
    for Ticker in ETF_dict.keys():
        if Ticker == 'SPY':
            continue
        else:
            exec("linreg.fit(SPY_daily_ret.values.reshape(-1,1)," +
                 Ticker+"_daily_ret.values.reshape(-1,1))")
            beta[Ticker] = float(linreg.coef_)

    beta_roll = pd.DataFrame(
        index=SPY_daily_ret.index[89:], columns=list(ETF_dict.keys())[1:])
    for Ticker in ETF_dict.keys():
        if Ticker == 'SPY':
            continue
        else:
            for i in range(89, len(SPY_daily_ret), 1):
                SPY_window = SPY_daily_ret.iloc[i-89:i]
                exec(Ticker+"_window = "+Ticker+"_daily_ret.iloc[i-89:i]")
                exec("linreg.fit(SPY_window.values.reshape(-1,1)," +
                     Ticker+"_window.values.reshape(-1,1))")
                beta_roll.ix[i-89, Ticker] = float(linreg.coef_)
    beta_roll.to_csv('beta_roll.csv')
    print("beta is saved in 'beta', 90-day rolling beta is saved in 'beta_roll'\n")
    # rolling 90-day's beta is not consistent over the entire period.
    # beta is not consistent with corr, because beta = corr * std(a) / std(b).

    '''Compute the auto-correlation of each ETF by regressing 
       each ETFs current days return against its previous days return'''
    auto_corr = {}
    for Ticker in ETF_dict.keys():
        exec("auto_corr['"+Ticker+"'] = "+Ticker+"_daily_ret.autocorr(lag=1)")
    print("auto-correlation of each ETF is saved in 'auto_corr'")
    # there's little auto-correlation evidence.

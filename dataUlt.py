import numpy as np
import pandas as pd 

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
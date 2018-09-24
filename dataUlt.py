import numpy as np
import pandas as pd 
import platform
import matplotlib.pyplot as plt

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

def import_yahoo_data(path, filename):
    '''input filename(ex.SPY), output df with date index'''
    if platform.system() == 'Darwin':
        filepath = path + '/data/' + filename + '.csv'
    else:
        filepath = path + '\\data\\' + filename + '.csv'
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

def import_fama_data(filename):
    '''input filename(ex.Fama_French_Three_Factors_Daily, output df with index)'''
    if platform.system() == 'Darwin':
        path = '/Users/xieyou/GitHub/MF803'
        filepath = path + '/data/' + filename
    else:
        path = 'C:\\Users\\47494\\GitHub\\MF803'
        filepath = path + '\\data\\' + filename
    df = pd.read_csv(filepath, header=1, names=['Date','Mkt-RF','SMB','HML','RF'])
    df['Date'] = pd.to_datetime(df['Date'].astype(str))
    df.set_index('Date', inplace=True)
    df = df / 100
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

def myhist(array):
    ''' input array, output histograph using Freedman-Diaconis method'''
    IQR = np.percentile(array, 75) - np.percentile(array, 25)
    # Freedman-Diaconis method
    width_of_bins = 2 * IQR / pow(len(array), 1/3)
    num_or_bins = int((max(array) - min(array)) / width_of_bins)
    plt.hist(array, bins=num_or_bins)
    plt.show()

def get_result(filename):
    if platform.system() == 'Darwin':
        path = '/Users/xieyou/GitHub/MF803'
        df = pd.read_csv(path + '/result/' + filename)
    else:
        path = 'C:\\Users\\47494\\GitHub\\MF803'
        df = pd.read_csv(path + '\\result\\' + filename)
    return df
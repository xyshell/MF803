import numpy as np 
import scipy.stats as si

class Instrument(object):
    '''
        define a financial Instrument 
    '''
    def __init__(self):
        pass
    
    def payoff(self, s_path):
        print (" method not defined for base class ")
        pass
    
    def price_rf(self, s_path, r):
        print (" method not defined for base class ")
        pass
    
    def price_bs(self, s0, r, sigma, T):
        print (" method not defined for base class ")
        pass

class EuropeanOpt(Instrument):
    '''
        define a European Option, input:
        pos : long or short, default is long
        kind : call or put, default is put
        k : strike price
    '''
    def __init__(self, k, pos='long', kind='call'):
        super(EuropeanOpt, self).__init__()
        self.k =  k
        self.pos = pos 
        self.kind = kind

    def payoff(self, s_path):
        ''' use underlying asset path to calculate payoff'''
        s_t = []
        for v in s_path.values():
            s_t = s_t.append(v[-1])
        if self.pos == 'long' and self.kind == 'call':
            return np.maximum(np.array(s_t) - self.k, 0)
        elif self.pos == 'long' and self.kind == 'put':
            return np.maximum(self.k - np.array(s_t), 0)
        elif self.pos == 'short' and self.kind == 'call':
            return -np.maximum(np.array(s_t) - self.k, 0)
        elif self.pos == 'short' and self.kind == 'put':
            return -np.maximum(self.k - np.array(s_t), 0)
    
    def price_rf(self, s_path, r):
        ''' calculate price using risk free discount'''
        return np.mean(self.payoff(s_path)) / (1+r)

class  LookbackOpt(Instrument):

    '''
        define a Lookback Option, input:
        pos : long or short, default is long
        kind : call or put, default is put
        k : strike price
    '''
    def __init__(self, k, pos='long', kind='call'):
        super(LookbackOpt, self).__init__()
        self.k =  k
        self.pos = pos 
        self.kind = kind

    def payoff(self, s_path):
        ''' use underlying asset path to calculate payoff'''
        s_min = []
        for v in s_path.values():
            s_min.append(np.min(v))
        if self.pos == 'long' and self.kind == 'call':
            return np.maximum(np.array(s_min) - self.k, 0)
        elif self.pos == 'long' and self.kind == 'put':
            return np.maximum(self.k - np.array(s_min), 0)
        elif self.pos == 'short' and self.kind == 'call':
            return -np.maximum(np.array(s_min) - self.k, 0)
        elif self.pos == 'short' and self.kind == 'put':
            return -np.maximum(self.k - np.array(s_min), 0)
    
    def price_rf(self, s_path, r):
        ''' calculate price using risk free discount'''
        return np.mean(self.payoff(s_path)) / (1+r)

class Straddle(Instrument):
    '''
        define a Straddle , input:
        k1 : put strike price 
        k2 : call strike price
        pos : long or short, default is long
    '''
    def __init__(self, k1, k2, pos='long'):
        super(Straddle, self).__init__()
        self.k1 = k1 
        self.k2 = k2
        self.pos = pos 

    def price_bs(self, s0, r, sigma, T):
        c_d1 = (np.log(s0 / self.k2) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        c_d2 = (np.log(s0 / self.k2) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        price_c = s0 * si.norm.cdf(c_d1, 0.0, 1.0) - si.norm.cdf(c_d2, 0.0, 1.0) * self.k2 * np.exp(-r * T)

        p_d1 = (np.log(s0 / self.k1) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        p_d2 = (np.log(s0 / self.k1) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        price_p = (self.k1 * np.exp(-r * T) * si.norm.cdf(-p_d2, 0.0, 1.0) - s0 * si.norm.cdf(-p_d1, 0.0, 1.0))
        return price_c + price_p
    
    def payoff(self, s_t):
        return np.maximum(np.array(s_t) - self.k1, 0) + np.maximum(self.k2 - np.array(s_t), 0)
        
if __name__ == '__main__':
    a = EuropeanOpt(100, 'long', 'put')
    from StochasticProcess import BlackScholes
    b = BlackScholes(s0 = 100, r = 0, sigma = 0.25, T = 1)
    b.simulation(1000)
    print(a.payoff(b.s_path))

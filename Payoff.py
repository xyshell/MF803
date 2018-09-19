import numpy as np 



class Instrument(object):
    '''
        define a financial Instrument 
    '''
    def __init__(self):
        pass
    
    def payoff(self, s_path):
        ''' use underlying asset path to calculate payoff'''
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
        
if __name__ == '__main__':
    a = EuropeanOpt(100, 'long', 'put')
    from StochasticProcess import BlackScholes
    b = BlackScholes(s0 = 100, r = 0, sigma = 0.25, T = 1)
    b.simulation(1000)
    print(a.payoff(b.s_path))

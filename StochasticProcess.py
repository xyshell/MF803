import numpy as np
import matplotlib.pyplot as plt

class StochasticProcess(object):
    ''' define a Stochastic Process, 1 day every step'''
    def __init__(self, s_t=[], s_path={}):
        self.s_t = s_t 
        self.s_path = s_path

    def random_generation(self, s):
        print (" method not defined for base class ")
        pass

    def simulation(self, n, is_show):
        print (" method not defined for base class ")
        pass

class BlackScholes(StochasticProcess):
    '''
        Black-Scholes Stochastic Process:
        dst = r * St * dt + sigma * St * dWt, 1 day every step, input:
        s0: intial asset price
        r: trend rate(annual)
        sigma: volality(annual)
        T: time range(year)
    '''

    def __init__(self, s0, r, sigma, T, s_t=[], s_path={}):
        super(BlackScholes, self).__init__(s_t, s_path)
        self.s0 = s0 
        self.r = r 
        self.sigma = sigma 
        self.T = T 

    def simulation(self, n, is_show=False):
        ''' 
            use monte carlo simulation to calculate 'n' asset paths
            is_show: draw picture of path or not, defalut is not.
        '''
        for i in range(n):
            price_list = [self.s0]
            daily_returns = np.random.normal(self.r/252, self.sigma/np.sqrt(252), 252*self.T)
            for x in daily_returns:
                price_list.append(price_list[-1]*(x+1))
            if is_show == True:
                plt.plot(price_list)
            self.s_t.append(price_list[-1])
            self.s_path[i] = price_list
        if is_show == True:
            plt.show()

class Bachelier(StochasticProcess):
    '''
        Bachelier Stochastic Process:
        dst = r * St * dt + sigma * dWt, 1 day every step, input:
        s0: intial asset price
        r: trend rate(annual)
        sigma: volality(annual)
        T: time range(year)
    '''

    def __init__(self, s0, r, sigma, T, s_t=[], s_path={}):
        super(Bachelier, self).__init__(s_t, s_path)
        self.s0 = s0 
        self.r = r 
        self.sigma = sigma 
        self.T = T 
    
    def random_generation(self, s):
        '''input S(t-1), calculate increment for St'''
        return np.random.normal(s*self.r/252, self.sigma/np.sqrt(252))

    def simulation(self, n, is_show=False):
        ''' 
            use monte carlo simulation to calculate 'n' asset paths
            is_show: draw picture of path or not, defalut is not.
        '''
        for i in range(n):
            price_list = [self.s0]
            for i in range(252*self.T):
                price_list.append(price_list[-1]+self.random_generation(price_list[-1]))
            if is_show == True:
                plt.plot(price_list)
            self.s_t.append(price_list[-1])
            self.s_path[i] = price_list
        if is_show == True:
            plt.show()

if __name__ == "__main__": 
    a = Bachelier(s0 = 100, r = 0.01, sigma = 0.25, T = 1)
    a.simulation(1000,is_show=True)
    print(a.s_path)
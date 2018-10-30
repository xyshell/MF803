import numpy as np 
import re
from sympy import solve, exp
from sympy import Symbol

class TermStructure(object):
    ''' define a term structure '''
    
    def __init__(self):
        pass

class SpotRate(TermStructure):
    ''' 
        points: dict
    '''
    def __init__(self, spot_rate_structure=None):
        super(SpotRate, self).__init__()
        self.spot_rate_structure = spot_rate_structure
        self.forward_rate_structure = self.spot2for().forward_rate_structure

    def spot2for(self):
        '''deduce forward structure from spot structure'''
        forward_rate_structure = dict()
        i = 0
        for key in spot_rate_structure.keys():
            if i == 0:
                key0 = '0Y'
                i = i + 1
            newkey = key0+'_'+key
            forward_rate_structure[newkey] = None
            key0 = key
        for key in forward_rate_structure.keys():
            A, B = key.split('_')
            a = int(re.findall('\d+',A)[0])
            b = int(re.findall('\d+',B)[0])
            if a == 0:
                forward_rate_structure[key] = spot_rate_structure[B]
                continue
            # f_a_b: forward rate from a to b
            s_a = spot_rate_structure[A]
            s_b = spot_rate_structure[B] 
            f_a_b = (s_b * b  - s_a * a) / (b - a)
            forward_rate_structure[key] = f_a_b
        return ForwardRate(forward_rate_structure)
    
    def find_disc_fact(T, self.forward_rate_structure):
        '''get discount factor from spot & forward structure'''
        t = int(re.findall('\d+',T)[0])
        interval = None
        if T in spot_rate_structure:
            return spot_rate_structure[T]
        else:
            for key, value in forward_rate_structure.items():
                A, B = key.split('_')
                a = int(re.findall('\d+',A)[0])
                b = int(re.findall('\d+',B)[0])
                if t > a and t < b:
                    interval = key
                    break 
            f_a_t = forward_rate_structure[interval]
            s_a = spot_rate_structure[A]
            s_t = (f_a_t*(t-a) +  s_a * a) / t
            return s_t

class ForwardRate(TermStructure):

    def __init__(self, forward_rate_structure):
        super(ForwardRate, self).__init__()
        self.forward_rate_structure = forward_rate_structure
    
    def for2spot(self, forward_rate_structure):
        '''deduce spot structure from forward structure'''
        spot_rate_structure = dict()
        for key in forward_rate_structure.keys():
            newkey = key.split('_')[1]
            spot_rate_structure[newkey] = None
        i = 0 
        for key in forward_rate_structure.keys():
            A, B = key.split('_')
            a = int(re.findall('\d+',A)[0])
            b = int(re.findall('\d+',B)[0])
            if a == 0:
                spot_rate_structure[B] = forward_rate_structure[key]
                continue
            # f_a_b: forward rate from a to b
            f_a_b = forward_rate_structure[key]
            s_a = spot_rate_structure[A]
            s_b =  (f_a_b * (b - a) + s_a * a) / b 
            spot_rate_structure[B] = s_b
        return SpotRate(spot_rate_structure)

class SwapRate(TermStructure):

    def __init__(self, points):
        super(SwapRate, self).__init__()
        self.points = points   

    def swap2spot(self, swap_rate_structure, freq=0.5):
        '''deduce spot structure from swap structure'''
        spot_rate_structure = dict.fromkeys(swap_rate_structure)
        par_value = 100
        for key in spot_rate_structure.keys():
            T = int(re.findall('\d+', key)[0])
            swap_rate = swap_rate_structure[key]
            x = Symbol('x', real=True)
            sum = 0
            for i in range(1,int(T/freq)+1):
                if i != T/freq:
                    a = par_value * swap_rate * freq * exp(-i*freq*x)
                    sum = sum + a 
                else:
                    a = (par_value * swap_rate * freq + par_value) * exp(-i*freq*x)
                    sum = sum + a 
            spot_rate_structure[key] = float(solve(sum - par_value, x)[0])
        return SpotRate(spot_rate_structure)

     
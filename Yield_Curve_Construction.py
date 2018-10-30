import numpy as np 
import re
from sympy import solve, exp
from sympy import Symbol

def swap2spot(swap_rate_structure, freq=0.5):
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
    return spot_rate_structure

def spot2for(spot_rate_structure):
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
    return forward_rate_structure

def for2spot(forward_rate_structure):
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
    return spot_rate_structure

def find_disc_fact(T, spot_rate_structure, forward_rate_structure):
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

def find_swap_rate(T, disc_fact, freq=0.5):
    '''get swap rate with T & disc_fact'''
    t = int(re.findall('\d+',T)[0])
    par_value = 100
    x = Symbol('x', real=True)
    sum = 0
    for i in range(1,int(t/freq)+1):
        if i != t/freq:
            a = x * freq * exp(-i*freq*disc_fact)
            sum = sum + a 
        else:
            a = (x * freq + par_value) * exp(-i*freq*disc_fact)
            sum = sum + a 
    swap_rate_t = float(solve(sum - par_value, x)[0])
    return swap_rate_t/100

def spot2swap(spot_rate_structure, freq=0.5):
    '''deduce swap structure from spot structure'''
    swap_rate_structure = dict.fromkeys(spot_rate_structure)
    for key in swap_rate_structure.keys():
        swap_rate_structure[key] = find_swap_rate(key, spot_rate_structure[key])
    return swap_rate_structure

if __name__ == "__main__": 
    swap_rate_structure = {'1Y':0.028438, '2Y':0.03060, 
        '3Y':0.03126,'4Y':0.03144, '5Y':0.03150, 
        '7Y':0.03169, '10Y':0.03210, '30Y':0.03237}

    spot_rate_structure = swap2spot(swap_rate_structure)
    forward_rate_structure = spot2for(spot_rate_structure)
    s_15 = find_disc_fact('15Y', spot_rate_structure, forward_rate_structure)
    swap_rate_15 =  find_swap_rate('15Y', s_15)

    # shift forward rates up 100 basis points
    forward_rate_structure_u = dict.fromkeys(forward_rate_structure)
    for key, value in forward_rate_structure.items():
        forward_rate_structure_u[key] = forward_rate_structure[key] + 0.01
    spot_rate_structure_u = for2spot(forward_rate_structure_u)
    swap_rate_structure_u = spot2swap(spot_rate_structure_u)

    # shift swap rate (1):
    swap_rate_structure_1 = {'1Y':0.028438, '2Y':0.03060, 
        '3Y':0.03126,'4Y':0.03194, '5Y':0.03250, 
        '7Y':0.03319, '10Y': 0.03460, '30Y':0.03737}
    spot_rate_structure_1 = swap2spot(swap_rate_structure_1)
    forward_rate_structure_1 = spot2for(spot_rate_structure_1)

    # shift swap rate (2):
    swap_rate_structure_2 = {'1Y':0.023438, '2Y':0.0281, 
        '3Y':0.02976,'4Y':0.03044, '5Y':0.03100, 
        '7Y':0.03169, '10Y':0.03210, '30Y':0.03237}
    spot_rate_structure_2 = swap2spot(swap_rate_structure_2)
    forward_rate_structure_2 = spot2for(spot_rate_structure_2)


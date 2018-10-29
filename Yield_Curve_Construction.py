import numpy as np 
import re
from sympy import solve, exp
from sympy import Symbol

def swap2spot(swap_rate_structure, freq=0.5):
    spot_rate_structure = dict.fromkeys(swap_rate_structure)
    par_value = 100
    for key in spot_rate_structure.keys():
        T = int(re.findall('\d+', key)[0])
        swap_rate = swap_rate_structure[key]
        x = Symbol('x', real=True)
        sum = 0
        for i in range(1,int(T/freq)+1):
            if i != T/freq:
                a = swap_rate * freq * exp(-i*freq*x)
                sum = sum + a 
            else:
                a = (swap_rate * freq + par_value) * exp(-i*freq*x)
                sum = sum + a 
        spot_rate_structure[key] = float(solve(sum - par_value, x)[0])
    return spot_rate_structure

def spot2for(spot_rate_structure):
    forward_rate_structrue = dict()
    i = 0
    for key in spot_rate_structure.keys():
        if i == 0:
            key0 = '0Y'
            i = i + 1
        newkey = key0+'_'+key
        forward_rate_structrue[newkey] = None
        key0 = key
    for key in forward_rate_structrue.keys():
        A, B = key.split('_')
        a = int(re.findall('\d+',A)[0])
        b = int(re.findall('\d+',B)[0])
        if a == 0:
            forward_rate_structrue[key] = spot_rate_structure[B]
            continue
        # f_a_b: forward rate from a to b
        s_a = spot_rate_structure[A]
        s_b = spot_rate_structure[B] 
        f_a_b = (s_b * b  - s_a * a) / (b - a)
        forward_rate_structrue[key] = f_a_b
    return forward_rate_structrue

# TODO: find swap rate at t=15Y 
# def find_swap_rate(spot_rate_structure, t, freq=0.5):
#     par_value = 100
#     x = Symbol('x', real=True)
#     sum = 0
#     for i in range(1,int(t/freq)+1):
#     if i != T/freq:
#         a = swap_rate * freq * exp(-i*freq*x)
#         sum = sum + a 
#     else:
#         a = (swap_rate * freq + par_value) * exp(-i*freq*x)
#         sum = sum + a 
#     spot_rate_structure[key] = float(solve(sum - par_value, x)[0])
#     return swap_rate_t

swap_rate_structure = {'1Y':2.8438, '2Y':3.060, 
    '3Y':3.126,'4Y':3.144, '5Y':3.150, 
    '7Y':3.169, '10Y': 3.210, '30Y':3.237}
# spot_rate_structure = {'1Y':2.824, '2Y':3.037,
#     '3Y':3.102,'4Y':3.120, '5Y':3.125,
#     '7Y':3.144, '10Y':3.185, '30Y':3.211}
par_value = 100
spot_rate_structure = swap2spot(swap_rate_structure)
forward_rate_structrue = spot2for(spot_rate_structure)

# forward_rate_structrue = dict.fromkeys(swap_rate_structure)
for key, value in forward_rate_structrue.items():
    print(key, value)
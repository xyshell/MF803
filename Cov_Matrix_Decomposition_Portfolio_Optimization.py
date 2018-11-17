import numpy as np 
import pandas as pd
from scipy.optimize import minimize
from matplotlib import pyplot as plt
from dataUlt import get_result, annual_matrix_rets


# ----------------- Problem 1 ----------------- #
# update ETFs return, delete SPY
matrix_daily_ret = get_result('ETFs_daily_ret.csv')
del matrix_daily_ret['SPY']

# calculate cov matrix of daily rets
cov_matrix_daily_ret = matrix_daily_ret.cov()
w,v = np.linalg.eig(cov_matrix_daily_ret.values)
w_sort = np.array(sorted(w,reverse=True))
plt.plot(w_sort, markersize=12, marker='o')
plt.title("eigenvalues in order")
plt.xlabel("order from largest to smallest")
plt.ylabel("eigenvalues")
#plt.show()
print(sum(w_sort > 0), 'eigenvalues are positive')
print(sum(w_sort < 0 ), 'eigenvalues are negative')
print(sum(w_sort == 0 ), 'eigenvalues are zero')

# simulate random cov matrix
sim_cov_matrix = np.random.normal(0, 1, (9,9))
w_sim, v_sim = np.linalg.eig(sim_cov_matrix)
w_sim_sort = np.array(sorted(w_sim,reverse=True))
plt.plot(w_sim_sort, markersize=12, marker='o')
plt.title("eigenvalues in order from simulation")
plt.xlabel("order from largest to smallest")
plt.ylabel("eigenvalues")
#plt.show()

# ----------------- Problem 2 ----------------- #
annual_rets = annual_matrix_rets(matrix_daily_ret,'d')
R = annual_rets.values
a = 1
n = R.shape[0]
w0 = np.ones(n) / n
C = (cov_matrix_daily_ret*252).values
U = lambda w: -(R.dot(w) - a * np.dot(np.dot(w, C),w))

w_bound = [(0, 1) for i in range(n)]
w_constraint = ({'type': 'eq', 'fun': lambda w: sum(w) - 1.})
res = minimize(U, w0, method = 'SLSQP', constraints = w_constraint, bounds = w_bound)
print(res.x)

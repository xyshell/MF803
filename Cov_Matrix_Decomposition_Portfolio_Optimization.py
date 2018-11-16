import numpy as np 
import pandas as pd
from matplotlib import pyplot as plt
from dataUlt import get_result

# update ETFs return, delete SPY
matrix_daily_ret = get_result('ETFs_daily_ret.csv')
del matrix_daily_ret['SPY']

# calculate cov matrix of daily rets
cov_matrix_daily_ret = matrix_daily_ret.cov()
w,v = np.linalg.eig(cov_matrix_daily_ret.values)
w_sort = np.array(sorted(w,reverse=True))
# TODO:add title, label
plt.plot(w_sort, markersize=12, marker='o')
plt.show()
print(sum(w_sort > 0), 'eigenvalues are positive')
print(sum(w_sort < 0 ), 'eigenvalues are negative')
print(sum(w_sort == 0 ), 'eigenvalues are zero')


pass


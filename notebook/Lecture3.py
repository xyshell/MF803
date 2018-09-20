'''
SQL resources:
– Database Programming in Python 
– SQL Programming
– SQL Server Docs
– PostgreSQL Docs

Test normality:
QQ plots(import statsmodels.api.qqplot)
Kolmogorov-Smirnov test(import statsmodels.kstest)

Cov random normal:
import numpy.random.multivariate normal

Stationary test:
statsmodels.tsa.stattools.adfuller

ARMA Models:
statsmodels.tsa.ARMA

raise exception:
if (sigma < 0):
    err = ValueError("Negative sigma provided") 
    raise err

'''
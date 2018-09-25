import numpy as np 
import matplotlib.pyplot as plt
from statsmodels.graphics.gofplots import qqplot
from StochasticProcess import BlackScholes, Bachelier
from Instrument import LookbackOpt
from dataUlt import myhist

Bachelier_a = Bachelier(r=0, s0=100, sigma=10.0, T=1)

# (a) 
Bachelier_a.simulation(1000, is_show=True)

# (b)
fig = plt.figure()
fig.suptitle("histogram of ending values of asset price")
myhist(np.array(Bachelier_a.s_t))
fig = qqplot(np.array(Bachelier_a.s_t))
fig.suptitle("qqplot of ending values of simulated paths")
plt.show()
print("the ending values of paths are normally distributed\n")

# (c)
LookbackOpt_a = LookbackOpt(k=100, pos='long', kind='put')
print("Bachelier: the price of a Lookback put option with k=100 is: ")
print(LookbackOpt_a.price_rf(Bachelier_a.s_path, Bachelier_a.r),'\n')

BlackScholes_a = BlackScholes(r=0, s0=100, sigma=0.1, T=1)
BlackScholes_a.simulation(1000)
print("BlackScholes: the price of a Lookback put option with k=100 is: ")
print(LookbackOpt_a.price_rf(BlackScholes_a.s_path, Bachelier_a.r),'\n')

# (d)
epsilon_list = [np.power(0.1,i) for i in range(18)]
delta_list = []
for epsilon in epsilon_list:
    Bachelier_u = Bachelier(r=0, s0=100+epsilon, sigma=10.0, T=1)
    Bachelier_u.simulation(1000)
    price_u = LookbackOpt_a.price_rf(Bachelier_u.s_path, Bachelier_u.r)
    Bachelier_d = Bachelier(r=0, s0=100-epsilon, sigma=10.0, T=1, s_delta=Bachelier_u.s_delta)
    Bachelier_d.simulation(1000)
    price_d = LookbackOpt_a.price_rf(Bachelier_d.s_path, Bachelier_d.r)
    delta_list.append((price_u - price_d) / (2 * epsilon))
print("let epsilon range from 0.1^0 to 0.1^17, calculate delta: \n", delta_list)
fig = plt.figure()
fig.suptitle("scatter of delta vs epsilon")
plt.scatter([i for i in range(len(delta_list))], delta_list)
plt.xlabel("0.1^n")
plt.ylabel("value of delta")
plt.show()
print("the value of delta remains more stable and precise " + 
    "when epsilon ranges from 0.1^3 to 0.1^9.\n" + 
    "when epsilon <=0.1^14, errors occurs, " +
    "and epsilon <= 0.1^15 leads to the largest amounts of error.")

'''
Question: 
epsilon_list = [np.power(0.1,i) for i in range(10)]
delta_list = []
for epsilon in epsilon_list:
    Bachelier_u = Bachelier(r=0, s0=100+epsilon, sigma=10.0, T=1)
    Bachelier_u.simulation(1000)
    price_u = LookbackOpt_a.price_rf(Bachelier_u.s_path, Bachelier_u.r)
    Bachelier_d = Bachelier(r=0, s0=100-epsilon, sigma=10.0, T=1, s_delta=Bachelier_u.s_delta)
    Bachelier_d.simulation(1000)
    price_d = LookbackOpt_a.price_rf(Bachelier_d.s_path, Bachelier_d.r)

    delta_list.append((price_u - price_d) / (2 * epsilon))
print(delta_list)
'''
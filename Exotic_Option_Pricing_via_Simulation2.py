import numpy as np 
from statsmodels.graphics.gofplots import qqplot

from StochasticProcess import BlackScholes, Bachelier
from Instrument import LookbackOpt
from dataUlt import myhist

Bachelier_a = Bachelier(r=0, s0=100, sigma=0.1, T=1)

# (a) Generate a series of normally distributed random numbers and use these to generate
# simulated paths for the underlying asset.   
Bachelier_a.simulation(1000, is_show=True)

# (b) Plot a histogram of the ending values of the asset price along the simulated paths.
# Are the ending values of your simulated paths normally distributed? 
# Check using your favorite normality test.
myhist(np.array(Bachelier_a.s_t))
qqplot(np.array(Bachelier_a.s_t))
print("the ending values of paths are...\n")


# (c) Calculate a simulation approximation to the price of a Lookback put option 
# with strike 100 under the Bachelier model. Compare the price of the lookback option 
# in the Bachelier model to the Black-Scholes model price obtained in HW1.
LookbackOpt_a = LookbackOpt(k=100, pos='long', kind='put')
print("Bachelier: the price of a Lookback put option with k=100 is: ")
print(LookbackOpt_a.price_rf(Bachelier_a.s_path, Bachelier_a.r),'\n')

BlackScholes_a = BlackScholes(r=0, s0=100, sigma=0.1, T=1)
BlackScholes_a.simulation(1000,is_show=False)
print("BlackScholes: the price of a Lookback put option with k=100 is: ")
print(LookbackOpt_a.price_rf(BlackScholes_a.s_path, Bachelier_a.r),'\n')




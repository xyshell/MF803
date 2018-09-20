from StochasticProcess import Bachelier

a = Bachelier(r=0, s0=100, sigma=0.1, T=1)

# (a) Generate a series of normally distributed random numbers and use these to generate
# simulated paths for the underlying asset.   
a.simulation(1000, is_show=True)

# (b) Plot a histogram of the ending values of the asset price along the simulated paths.
# Are the ending values of your simulated paths normally distributed? 
# Check using your favorite normality test.

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as si

'''Generate a series of normally distributed random numbers and 
   use these to generate simulated paths for the underlying asset'''
def monte_carlo_simulation(s0, r, sigma, T, n, is_show=False):
    ''' dst = r * St * dt + sigma * St * dWt, 1 day every step, input:
        s0: intial asset price
        r: trend rate(annual)
        sigma: volality(annual)
        T: time range(year)
        n: number of paths
        is_show: draw picture of path or not, defalut is not.
    '''
    st = []
    smin = []
    spath = {}
    for i in range(n):
        daily_returns = np.random.normal(r/252, sigma/np.sqrt(252), 252*T)
        price_list = [s0]
        for x in daily_returns:
            price_list.append(price_list[-1]*(x+1))
        plt.plot(price_list)
        st.append(price_list[-1])
        smin.append(min(price_list))
        spath[i] = price_list
    if is_show == True: 
        plt.show()
    return spath, st, smin

if __name__ == '__main__':

    s0 = 100
    r = 0
    sigma = 0.25
    T = 1
    n = 1000

    spath, st, smin = monte_carlo_simulation(s0, r, sigma, T, n, True)
    st_mean = np.mean(st)
    st_var = np.var(st)
    print("St mean is ", st_mean, ",\nSt var is ", st_var)

    # theoretically, the mean should be 100, and the var should be 625.
    # The result is almost consist with the theory.

    '''Calculate the payoffs of a European put option with strike 100
       along all simulated paths. Make a histogram of the payoffs for
       the European option.'''
    k = 100
    payoff_put_opt = np.maximum(k - np.array(st), 0)
    IQR = np.percentile(payoff_put_opt, 75) - np.percentile(payoff_put_opt, 25)
    # Freedman-Diaconis method
    width_of_bins = 2 * IQR / pow(len(payoff_put_opt), 1/3)
    num_or_bins = int((max(payoff_put_opt) - min(payoff_put_opt)) / width_of_bins)
    plt.hist(payoff_put_opt, bins=num_or_bins)
    plt.show()
    payoff_mean = np.mean(payoff_put_opt)
    payoff_std = np.std(payoff_put_opt)
    print("payoff mean is", payoff_mean, ",\npayoff std is ", payoff_std)

    # the stds are almost about 12.25, the means of payoff are almost about 10.

    '''Calculate a simulation approximation to the price of a European put option
       by taking the average discounted payoff across all paths.'''
    prc_put_opt = np.mean(payoff_put_opt) / (1+r)
    print("price of put option based on averagely discount is ", prc_put_opt)

    '''Compare the price of the European put option obtained via simulation
       to the price you obtain using the Black-Scholes formula.'''
    d1 = (np.log(s0 / k) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(s0 / k) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    prc_put_opt_bs = (k * np.exp(-r * T) * si.norm.cdf(-d2, 0.0,
                                                       1.0) - s0 * si.norm.cdf(-d1, 0.0, 1.0))
    print("price of put option based on BS formula is ", prc_put_opt_bs)

    # the prices based on average discount and on BS formula are similar

    '''Calculate the payoff of a fixed strike lookback put option with stike 100
       along all simulated path, and its simulation price by averagely discount.'''

    payoff_exo_opt = np.maximum(k - np.array(smin), 0)
    prc_exo_opt = np.mean(payoff_exo_opt) / (1+r)
    print("price of lookback put option is ", prc_exo_opt)

    '''Calculate the premium that the buyer is charged for the extra optionality embedded in
    the lookback. When would this premium be highest? Lowest? Can it ever be negative?'''

    premium = payoff_exo_opt - payoff_put_opt
    print("the highest premium is ", max(premium), ",\nthe lowest premium is ", min(premium))
    plt.plot(spath[np.argmax(premium)], label='Highest Premium')
    plt.plot(spath[np.argmin(premium)], label='Loweset Premium')
    plt.legend()
    plt.show()

    # the highest premium occurs when asset price goes down hugely,
    # but eventually turns back quite a lot at expiracy.
    # the lowest premium occurs when st is actually the lowest price.
    # the premium can never be negative because min(spath) >= st

    '''Try a few different values of sigma and comment on what happens to the price of the
    European, the Lookback option and the spread/premium between the two.'''

    sigma2 = 0.4

    spath, st, smin = monte_carlo_simulation(s0, r, sigma2, T, n)
    payoff_put_opt = np.maximum(k - np.array(st), 0)
    prc_put_opt = np.mean(payoff_put_opt) / (1+r)
    print("with new sigma, price of put option based on averagely discount is", prc_put_opt)

    d1 = (np.log(s0 / k) + (r + 0.5 * sigma2 ** 2) * T) / (sigma2 * np.sqrt(T))
    d2 = (np.log(s0 / k) + (r - 0.5 * sigma2 ** 2) * T) / (sigma2 * np.sqrt(T))
    prc_put_opt_bs = (k * np.exp(-r * T) * si.norm.cdf(-d2, 0.0,
                                                       1.0) - s0 * si.norm.cdf(-d1, 0.0, 1.0))
    print("with new sigma, price of put option based on BS formula is ", prc_put_opt_bs)

    payoff_exo_opt = np.maximum(k - np.array(smin), 0)
    prc_exo_opt = np.mean(payoff_exo_opt) / (1+r)
    print("with new sigma, price of lookback put option is", prc_exo_opt)

    premium = payoff_exo_opt - payoff_put_opt
    print("with new sigma, the highest premium is ", max(premium),
        ",\nthe lowest premium is ", min(premium))

    # if increasing the sigma, the price of options would increase, the premium would increase,
    # is decreasing the sigma, the price of options would decrease, the premium would decrease.

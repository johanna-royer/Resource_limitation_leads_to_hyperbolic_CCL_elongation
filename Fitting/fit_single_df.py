'''FIT SINGLE DATAFRAME

This script can be run on a single data frame to fit the hyperbolic function with
and without variability. A standardized data set must be used for this script. The
example here is shown with specifications for the zebrafish data set used in my master's thesis. '''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# hyperbolic function used for fitting
def hyperbolic_function(S, l, S_G, L_mu):
    return(l/(S_G-S)) + L_mu


# read data 
filepath = "FILE PATH"
data_dict = pd.read_excel(filepath, sheet_name = None)

# define data set and species name
df = data_dict['Zebrafish']
species_name = r'$D. rerio$'

# show data in a scatterplot with error bars
plt.errorbar(df['generation'], df['mean'], yerr = df['std'], fmt="o", color="royalblue", capsize=2, label = species_name)

# estimate optimized parameters fitting mean values only (main method)
popt, pcov = curve_fit(hyperbolic_function, df['generation'], df['mean'], p0 = (0,15,0), maxfev = 50000)

# estimate optimized parameters fitting mean and variability (sd) values
popt_sig, pcov_sig = curve_fit(hyperbolic_function, df['generation'], df['mean'], sigma = df['std'], absolute_sigma=True, p0 = (0,15,0), maxfev = 50000)

# simulate data using the estimated optimized parameters
x = np.linspace(0, 15, 100)
y = hyperbolic_function(x, *popt)
y_sig = hyperbolic_function(x, *popt_sig)

# plot the simulated hyperbolic function 
plt.plot(x, y, color = 'r', alpha = 0.5, linestyle = '--', label = 'fit without sigma')
plt.plot(x, y_sig, color = 'g', alpha = 0.5, linestyle = '--', label = 'fit with sigma')
plt.ylim(0, 80)

# create simulated values for the given generations for r2 score calculations 
# and show in a scatter plot 
test = hyperbolic_function(df['generation'], *popt)
plt.scatter(df['generation'], test, color = 'red', label = 'predicted values without sigma')

test_sig = hyperbolic_function(df['generation'], *popt_sig)
plt.scatter(df['generation'], test_sig, color = 'green', label = 'predicted values with sigma')

# calculate r2 scores
r2 = r2_score(df['mean'], test)
print('r2 without sigma = ', r2)

r2_sig = r2_score(df['mean'], test_sig)
print('r2 with sigma = ', r2_sig)

# show the data and fits
plt.xlabel('Generation $s$')
plt.ylabel('Cell cycle length $L$ (min)')
plt.legend()
plt.show()
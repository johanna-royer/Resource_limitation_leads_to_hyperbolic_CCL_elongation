import matplotlib.pyplot as plt
import scipy.stats
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

''' COMPARISON OF MEAN AND VARIABILITY FIT

In this script, the two different fit options are compared - mean and variability fits.
The values used for comparison are rounded optimized values obtained by fitting (see Fitting.individual_fits.py)
'''



species_colors = ['green', 'black', 'crimson', 'm', 'blue', 'darkorange', 'firebrick', 'mediumpurple']
species_markers = ['^','o', 'h', 'd', 'v', 'p', '*', 's']


ax_spine_thickness = 1.5
label_ticksize = 18
marker_size = 80
legend_fontsize = 18
text_fontsize = 18
label_fontsize = 18
marker_linewidth = 2


fig, (ax1, ax2, ax3) = plt.subplots(nrows = 1, ncols = 3, figsize = (12,4))


ax1.spines.bottom.set_linewidth(ax_spine_thickness)
ax1.spines.left.set_linewidth(ax_spine_thickness)
ax1.spines.top.set_linewidth(ax_spine_thickness)
ax1.spines.right.set_linewidth(ax_spine_thickness)

ax2.spines.bottom.set_linewidth(ax_spine_thickness)
ax2.spines.left.set_linewidth(ax_spine_thickness)
ax2.spines.top.set_linewidth(ax_spine_thickness)
ax2.spines.right.set_linewidth(ax_spine_thickness)

ax3.spines.bottom.set_linewidth(ax_spine_thickness)
ax3.spines.left.set_linewidth(ax_spine_thickness)
ax3.spines.top.set_linewidth(ax_spine_thickness)
ax3.spines.right.set_linewidth(ax_spine_thickness)


ax1.tick_params(axis = 'both', which = 'major', labelsize = label_ticksize)
ax2.tick_params(axis = 'both', which = 'major', labelsize = label_ticksize)
ax3.tick_params(axis = 'both', which = 'major', labelsize = label_ticksize)


# s* comparison
plt.subplot(1, 3, 1)

mean_fit = [13.85, 15.44, 5.51, 5.36, 14.43, 13.34, 9.42, 15.67]
var_fit = [13.60, 15.09, 5.30, 5.36, 14.45, 13.00, 9.33, 15.43]

for i, element in enumerate(mean_fit):
    plt.scatter(mean_fit[i], var_fit[i], marker = species_markers[i], facecolor = 'white', edgecolors = species_colors[i], linewidth = marker_linewidth, s = marker_size)

plt.xlabel(r'$s^*$', fontsize = label_fontsize)
#plt.ylabel(r'$s^*$ mean and variability fit ', fontsize = 12)

def func(x, k, d):
    y = k*x + d
    return y

popt, pcov = curve_fit(func, mean_fit, var_fit)
print(popt)
print(pcov)
x_fit1 = np.linspace(0, 16, 100)
y_fit1 = func(x_fit1, *popt)
plt.plot(x_fit1, y_fit1, linestyle = '--', color = 'black', alpha = 0.5, label = r'$R^2$ = 0.99')
plt.legend(fontsize = legend_fontsize)
p = np.corrcoef(mean_fit, var_fit)
print('corrcoef s* = ', p)

r = scipy.stats.pearsonr(mean_fit, var_fit)
print('pearson scipy: ', r)


test = func(np.array(mean_fit), *popt)
r2 = r2_score(mean_fit, test)
print('r2: ', r2)
# Lambda comparison
plt.subplot(1, 3, 2)

mean_fit = [42.96, 105.45, 6.60, 31.11, 23.39, 105.85, 41.80, 110.79]
var_fit = [29.47, 76.97, 3.93, 31.11, 24.65, 86.87, 33.90, 98.82]

for i, element in enumerate(mean_fit):
    plt.scatter(mean_fit[i], var_fit[i], marker = species_markers[i], facecolor = 'white', edgecolors = species_colors[i], linewidth = marker_linewidth, s = marker_size)

plt.xlabel(r'$\Lambda$ ', fontsize = label_fontsize)
#plt.ylabel(r'$\Lambda$ mean and variability fit', fontsize = 12)

popt, pcov = curve_fit(func, mean_fit, var_fit)
print(popt)
print(pcov)
x_fit2 = np.linspace(0, 120, 120)
y_fit2 = func(np.array(x_fit2), *popt)
plt.plot(x_fit2, y_fit2, linestyle = '--', color = 'black', alpha = 0.5, label =  r'$R^2$ = 0.89')
plt.legend(fontsize = legend_fontsize)

r = scipy.stats.pearsonr(mean_fit, var_fit)
print('pearson scipy: ', r)

test = func(np.array(mean_fit), *popt)
r2 = r2_score(mean_fit, test)
print('r2: ', r2)

# Lambda comparison
plt.subplot(1, 3, 3)
mean_fit = [8.70, 64.97, 13.73, 44.69, 3.23, 34.96, 32.51, 18.15]

var_fit = [11.32, 68.67, 13.83, 44.69, 2.13, 36.99, 33.96, 18.11]
for i, element in enumerate(mean_fit):
    plt.scatter(mean_fit[i], var_fit[i], marker = species_markers[i], facecolor = 'white', edgecolors = species_colors[i], linewidth = marker_linewidth, s = marker_size)

plt.xlabel(r'$L_{\mu}$', fontsize = label_fontsize)

fig.text(0.52, -0.005, 'mean fit', ha='center', fontsize = text_fontsize)
fig.text(0.01, 0.58, 'mean and variability fit', va='center', rotation='vertical', fontsize = text_fontsize)

r = scipy.stats.pearsonr(mean_fit, var_fit)
print('pearson scipy: ', r)

popt, pcov = curve_fit(func, mean_fit, var_fit)
print(popt)
print(pcov)
x_fit3 = np.linspace(0, 70, 100)
y_fit3 = func(x_fit3, *popt)
plt.plot(x_fit3, y_fit3, linestyle = '--', color = 'black', alpha = 0.5, label = r'$R^2$ = 0.99')
plt.legend(fontsize = legend_fontsize)

test = func(np.array(mean_fit), *popt)
r2 = r2_score(mean_fit, test)
print('r2: ', r2)

plt.tight_layout()
plt.savefig('ComparisonMeanVarFit.png', dpi = 1200)
plt.show()
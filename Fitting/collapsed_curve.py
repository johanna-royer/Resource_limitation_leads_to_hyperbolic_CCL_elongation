'''COLLAPSED CURVE

This code section creates the collapsed hyperbolic curve with normalized values (normalization by the minimum CCL and the generation of the singularity). 
'''

import utils.visualization as vis
import matplotlib.pyplot as plt
import pandas as pd
import utils.normalization as norm 
import numpy as np
from utils.model import hyperbolic_function
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score



# load data
filepath = "C:/Users/johan/Documents/Biologie Master/Projektlabor Cell Cycle Elongation/Data/Raw data reproducible/Data_combined_from_raw_files.xlsx"
data_dict = pd.read_excel(filepath, sheet_name = None)


# Pre-processing
data_dict['Axolotl Dataset 1'] = data_dict['Axolotl Dataset 1'][data_dict['Axolotl Dataset 1']['generation'] < 15]
data_dict['Axolotl Dataset 2'] = data_dict['Axolotl Dataset 2'][data_dict['Axolotl Dataset 2']['generation'] < 15]
data_dict['C elegans full'] = data_dict['C elegans full'][data_dict['C elegans full']['generation'] < 6]
data_dict['Nematostella'] = data_dict['Nematostella'][data_dict['Nematostella']['generation'] < 11]
data_dict['Dreissena'] = data_dict['Dreissena'][data_dict['Dreissena']['generation'] < 6]

df_results_one_per_species = pd.read_csv('results_one_per_species.csv')

fig2_species_collapsed_curve = ['Zebrafish', 'Axolotl Dataset 1', 'Axolotl Dataset 2', 'Drosophila Study 1','C elegans full', 'Dreissena', 'Drosophila Study 2', 'Drosophila Study 3', 'Nematostella', 'Sea urchin', 'Xenopus Study 1',  'Xenopus Study 2',  ]

vis.plot_layout(figsize = (12, 7))
plt.ylabel(r'$L/L_{min}$', fontsize = 20)
plt.xlabel(r'$s/s^*$', fontsize  = 20)

s_normalized_combined = []
duration_normalized_combined = []
species_list_normalized = []


prev_species = None

for element in fig2_species_collapsed_curve:
    df = data_dict[element]

    species = df['species'][0]


    s_normalized, duration_normalized = norm.normalized_results(df, 1, prev_species = prev_species, element = element, df_results_one_per_species = df_results_one_per_species, s_normalizer = 'species_s*')

    s_normalized_combined = s_normalized_combined + list(s_normalized)
    duration_normalized_combined = duration_normalized_combined + list(duration_normalized)

    for i in range(len(list(s_normalized))):
        species_list_normalized.append(species)

    
    prev_species = species

popt, pcov = curve_fit(hyperbolic_function,s_normalized_combined, duration_normalized_combined, p0 = (0,15,0), maxfev = 50000) 
l_opt, S_g_opt, L_mu_opt = popt                          

print(popt)


Cleavage_Fit = np.linspace(0, 0.99, 100)
Duration_Fit = hyperbolic_function(Cleavage_Fit, *popt)

y_pred = hyperbolic_function(s_normalized_combined, *popt)
r2 = r2_score(duration_normalized_combined, y_pred)

plt.plot(Cleavage_Fit, Duration_Fit, linewidth = 3, alpha = 0.5, color = 'black', linestyle = '--', label = r'$R^2$ = 0.93') 
plt.vlines(1, 0, 7, color = 'red', linestyle = '--', linewidth = 3, alpha =0.5)

plt.legend(prop={'style': 'italic', 'size': 14}, frameon = False )
plt.xlim(0.0, 1.1)
plt.ylim(0.0,7)
#plt.tight_layout(rect=[0, 0.1, 1, 1])  # reduce right space to 85% width
vis.save_figures('Results_collapsed.png', save = True)
print(r'$R^2$ score: ', r2)
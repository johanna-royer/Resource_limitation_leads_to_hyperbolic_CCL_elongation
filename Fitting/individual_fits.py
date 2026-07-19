'''INDIVIDUAL FITS 

WORKFLOW
1) read data from raw data file*
2) apply pre-processing steps as described in the methodology of the master's thesis
3) iterate through data sets - combine several data sets for the same species into one
4) fit the combined data with the hyperbolic function - save optimized parameters in a DataFrame "results_one_per_species"
5) fit individual data sets with hyperbolic function - save optimized parameters in a DataFrame "results"
6) plot the data as a scatter plot with error bars and the simulated hyperbolic curve using optimized parameters
7) save optimized parameters in .csv files 
'''

# Import packages 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import utils.visualization as vis
import utils.fitting as fit
from utils.model import hyperbolic_function


# load data
filepath = "C:/Users/johan/Documents/Biologie Master/Projektlabor Cell Cycle Elongation/Data/Raw data reproducible/Data_combined_from_raw_files.xlsx"
data_dict = pd.read_excel(filepath, sheet_name = None)


# additional preprocessing as described for each data set in the methods section 
data_dict['Axolotl Dataset 1'] = data_dict['Axolotl Dataset 1'][data_dict['Axolotl Dataset 1']['generation'] < 15]
data_dict['Axolotl Dataset 2'] = data_dict['Axolotl Dataset 2'][data_dict['Axolotl Dataset 2']['generation'] < 15]
data_dict['C elegans full'] = data_dict['C elegans full'][data_dict['C elegans full']['generation'] < 6]
data_dict['Nematostella'] = data_dict['Nematostella'][data_dict['Nematostella']['generation'] < 11]
data_dict['Dreissena'] = data_dict['Dreissena'][data_dict['Dreissena']['generation'] < 6]

# create list to save fitting results in (later to be converted into a dataframe and saved as an excel file)
results = []
results_one_per_species = []

# list of datasets -> bc then I can access through index, rather than just dictionary name 
dataset_list = list(data_dict)
# same for species -> so I can use the index to access the previous and especially the species of the next dataset
species_list = list(data_dict[entry]['species'][0] for entry in data_dict)

# loop through all dataframes to plot individual 

prev_species = None                                     # set a variable for saving the species of the last iteration to None in the beginning and then change in the following loop
for index, entry in enumerate (data_dict):
    print(index, entry)

    

    species = data_dict[entry]['species'][0]            # define the current species (dataset of the current iteration)



        
    if species == prev_species:                         # if the current species is the same as the previous, then the rest of the steps should be skipped
        continue                                        # (bc everything else was already done the first time the species occurred)

    

    if index == 0 or species != prev_species:           # only create a new plot if it is the first dataset or if the current species is different from the previous one (so that data from the same species is plotted in one figure)
        vis.plot_layout()
        plt.xlabel(r'Generation $s$', fontsize = 26)
        plt.ylabel('CCL (min)', fontsize = 26)

            

    
    species_counter = 0

    # find out all the datasets with data for this species and save them in a list of datatframes
    dfs = []
    for counter, species_name in enumerate(species_list):                                               # go through the list of the occuring species as they appear in the dataset
        if species_name == species:
            current_df = data_dict[dataset_list[counter]]    
            
            if species == 'C. elegans':
                current_df = current_df[current_df['generation'] > 1].reset_index()
                print(current_df)

            else:                                          # if the species are the same, rescale the df by dropping the first few, longer generations
                current_df = fit.drop_first_generations(current_df)

            L_min = min(current_df['mean'])
            print(L_min)
            #gen_start = current_df[current_df['mean']== L_min]['generation']
            popt, pcov = curve_fit(hyperbolic_function, current_df['generation'], current_df['mean'], p0 = (0,15,0), maxfev = 50000) 
            l_opt, S_g_opt, L_mu_opt = popt   
            print(entry)
            results.append((entry, species, L_min,  l_opt, S_g_opt, L_mu_opt)) #gen_start[0].astype(int),

            dfs.append(current_df)                                                           # add the data to a list of dataframes later to be combined into 1 for the fitting
            fit.scatterplot_species(current_df, (index + species_counter))                       # then create the individual scatterplot-points but in combined plots -> the counter is there so that the label moves on while the variable "index" remains the same 
            species_counter += 1                                                             # increase counter (of how many datasets have been added for this species)

    # now combine all the datasets that belong to one species (if there is only one then only the one df will be in the list)
    df = pd.concat(dfs, ignore_index = True)

    # and fit the hyperbolic growth function, determining the best fitting values for lambda, s*, and L_mu
    popt, pcov = curve_fit(hyperbolic_function, df['generation'], df['mean'], p0 = (0,15,0), maxfev = 50000) 
    l_opt, S_g_opt, L_mu_opt = popt   
    
    results_one_per_species.append((species, float(l_opt), S_g_opt, L_mu_opt))

    # plot the resulting fit using the optimized parameters 
    fit.fitting_plot(df, popt)
    




    vis.save_figures(f'{species}_ind.png', dpi = 1200)  
    
    # at the end of the iteration, set prev_species to the current species so this information is available in the next iteration of the loop
    prev_species = species                              

plt.show()

results_df = pd.DataFrame(results, columns = ['Data set', 'L_min', 'Species', 'Lambda', 's*', 'L_mu'])
results_one_per_species_df = pd.DataFrame(results_one_per_species, columns = ['Species', 'Lambda', 's*', 'L_mu'])

results_df.to_csv("results.csv", header=True, index=False)
results_one_per_species_df.to_csv("results_one_per_species.csv", header=True, index=False)


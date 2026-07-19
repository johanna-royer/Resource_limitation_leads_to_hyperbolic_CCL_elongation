import matplotlib.pyplot as plt
import utils.visualization as vis
import utils.config as config
import numpy as np
from utils.model import hyperbolic_function
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score


def identify_shortest_cycle(df):
    """Identify the shortest cell cycle and generation it occurs in 

    Args:
        df (pandas.DataFrame): data frame containing the generation s and mean CCL values

    Returns:
        L_min (float): duration of the shortest cell cycle
        gen_start (int): generation of the shortest cell cycle 
    """        
        
    # identify the shortest cell cycle 
    L_min = min(df['mean'])
    # identify the generation with the shortest cell cycle length                                          
    gen_start = int(df[df['mean'] == min(df['mean'])]['generation'].iloc[0])   

    return (L_min, gen_start)

def drop_first_generations(df):   

        """
        Drop all generations before the one with the minimum cell cycle length from a dataframe

        Parameters
        ----------
         df: pandas.DataFrame
             dataframe containing at least information for cell cycle duration and generation 
             with all given datapoints included 

         Returns 
         pandas.DataFrame
            A new DataFrame including only the values for generations starting from the one with 
            the minimum cell cycle length
        """ 

        # identify the generation with the shortest cell cycle length                                          
        L_min, gen_start = identify_shortest_cycle(df)
        
        # keep only the generations from the generation with the shortest cell cycle length onward
        df = df[df['generation'] >= gen_start]     

        # reset index of the new DataFrame and drop to avoid saving index in new column                    
        df = df.reset_index(drop = True)                                                     

        return df


def scatterplot_species(df, index):

    """Plot the mean and std of CCL over the generation s for a given df

    Args:
        df (pandas.DataFrame): data frame containing the generation s and mean CCL values
        index (int): index in the data set list refers to the correct species name 

    """    

    label = config.dataset_list[index]
    species = df['species'][0]

    species_color = vis.species_colors[label]
    species_marker = vis.species_markers[species]

    plt.errorbar(df['generation'], df['mean'], df['std'], capsize = 5, fmt = 'none', color = 'black', zorder = 1, alpha = 0.5, linewidth = 2)
    plt.scatter(df['generation'], df['mean'], label = label, edgecolors = species_color, facecolor = 'white', marker = species_marker, linewidth = 3, s = 120, zorder = 2)
    
    plt.legend(fontsize = 18)


def fitting_plot(df, popt):
    """_summary_

    Args:
        df (pandas.DataFrame): data frame containing the generation s and mean CCL values
        popt (tuple): contains the optimal parameters obtained by model fitting 
    """    

    l_opt, S_g_opt, L_mu_opt = popt   

    # scaling of plot: first determine max. x-value, then minimum y-values based on % of the shown data
    max_gen = int(df[df['mean'] == max(df['mean'])]['generation'].iloc[0])

    # go to 60% of the difference between the optimal fit value for s* (S_g_opt) and the maximum generation of the dataset
    fit_max = S_g_opt - (S_g_opt - max_gen) *0.5

    # for the minimum y-value take 70% of the value of the lower bound of the errorbar of the minimum CCL 
    min_value = ((min(df['mean'])) - df['std'].iloc[0]) * 0.7
    # set the lower bound of the y-axis to this calculated minimum value 
    plt.ylim(min_value, None)

    Cleavage_Fit = np.linspace(min(df['generation']), fit_max)              # create array of values for s as input for the hyperbolic function with optimized parameters 
    Duration_Fit = hyperbolic_function(Cleavage_Fit, *popt)                 # calculate the hyperbolic function values for the argument Cleavage_Fit and the optimized parameters
    plt.plot(Cleavage_Fit, Duration_Fit, color = 'black', linewidth = 4, alpha = 0.7, label = 'Fit', zorder = 1, linestyle = '--')

    # line marking the singularity should go from the minimum y value to either the same height as the fit function or up to the value of the last datapoint + std
    max_y_value = (max(df['mean']))# + max(df['std']))
    plt.vlines(S_g_opt, min_value, max(Duration_Fit[-1], max_y_value),  color = 'red', linestyle = '--', linewidth = 4, alpha = 0.6, label = 'Singularity')
    plt.legend(prop={'style': 'italic', 'size': 18})

    # plt.tight_layout(rect=[0, 0, 0.90, 1])



def normalized_plot(df, species_color, species_marker):
    """Create collapsed curve by normalizing valus

    Normalizations are performed
    - by dividing by the minimum CCL on the y-axis
    - by dividing by the generation of the maximum generation on the x-axis 

    Args:
        df (pandas.DataFrame): data frame containing the generation s and mean CCL values
        species_color (str): color associated with the current species
        species_marker (str): marker associated with the current species 
    """    


    L_min = min(df['mean'])
    duration_normalized = df['mean']/L_min
    s_max = max(df['generation'])
    s_normalized = df['generation']/s_max

    species = df['species'][0]


    #plt.errorbar(s_normalized, duration_normalized, df['std'], capsize = 4, fmt = 'none', color = 'black', zorder = 1, alpha = 0.5)
    plt.scatter(s_normalized, duration_normalized, label = species, edgecolors = species_color, facecolor = 'white', marker = species_marker, linewidth = 1.5, s = 60, zorder = 2)
    
    
    popt, pcov = curve_fit(hyperbolic_function, s_normalized, duration_normalized, p0 = (0,15,0), maxfev = 50000) 
    l_opt, S_g_opt, L_mu_opt = popt                         # extract fitting parameters 
    Cleavage_Fit = np.linspace(min(s_normalized), max(s_normalized))
    Duration_Fit = hyperbolic_function(Cleavage_Fit, *popt)
    
    plt.plot(Cleavage_Fit, Duration_Fit, color = species_color, linewidth = 2, alpha = 0.5)
    plt.legend(prop={'style': 'italic', 'size': 22})
    plt.tight_layout(rect=[0, 0, 0.90, 1])


import utils.fitting as fit
from utils.model import hyperbolic_function
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import utils.visualization as vis


normalized_results_defaults = {
    'prev_species': None, 
    'L_normalizer': 'L_min', 
    's_normalizer': 's*'
}


def normalized_results(df, sG, element, df_results_one_per_species, **kwargs):
    """Create normalized values for the CCL L and the generation s 

    Normalization can be specified (defaults = L_min, s*):
        1) L_normalizer = L_min (minimum CCL) or L0 (Lambda/sG+L_mu) or L_mu (optimized value)
        2) s_normalizer = s* (predicted singularity) or sG (literature value)

    Args:
        df (pandas.DataFrame): individual species df
        sG (float): literature value for the generation of gastrulation onset
        element (str): data set name
        df_results_one_per_species (pandas.DataFrame): data frame containing the optimized values from individual fittings 

    Returns:
        s_normalized, duration_normalized (numpy.arrays): generation normalized by s_normalizer and L_normalizer
    """    

    df = fit.drop_first_generations(df)
    popt, pcov = curve_fit(hyperbolic_function, df['generation'], df['mean'], p0 = (0,15,0), maxfev = 50000)  
    l_opt, S_g_opt, L_mu_opt = popt  

    params = normalized_results_defaults.copy()
    params.update(kwargs)

    species = df['species'][0]

    species_color = vis.species_colors[element]
    species_marker = vis.species_markers[species]
    
    L_min = min(df['mean'])             # identify the duaration of the minimum cell cycle for L_normalizer = L_min
    L0 = l_opt/S_g_opt+L_mu_opt         # compute L0 for L_normalizer = L0
    
    # specify normalizers for L and s
    L_normalizer = params['L_normalizer']
    if L_normalizer == 'L_min': 
         L_normalizer = L_min
    elif L_normalizer == 'L0':
         L_normalizer = L0
    elif L_normalizer == 'L_mu':
          L_normalizer = L_mu_opt
    else: 
         print("Error: Invalid normalizer for L")
         
    s_normalizer = params['s_normalizer']
    if s_normalizer == 's*':
         s_normalizer = S_g_opt
    elif s_normalizer == 'sG':
         s_normalizer = vis.sg_literature_values[species]
    elif s_normalizer == 'species_s*':
         s_normalizer = df_results_one_per_species[df_results_one_per_species['Species'] == species]['s*'].reset_index(drop = True)
         s_normalizer = float(s_normalizer[0])
    else:
         print("Error: Invalid normalizer for s")

    # calculate normalized values
    duration_normalized = df['mean']/L_normalizer
    s_normalized = df['generation']/s_normalizer

    if species == params['prev_species']:
        label = None
    else:
         label = vis.species_name_dict[species]
    
    # show normalized values in a scatter plot 
    plt.scatter(s_normalized, duration_normalized, label = label, edgecolors = species_color, facecolor = 'white', marker = species_marker, linewidth = 1.5, s = 60, zorder = 2)

    return (s_normalized, duration_normalized)

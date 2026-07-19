import matplotlib.pyplot as plt 


# Sizes and defaults
LABEL_FONTSIZE = 20
LEGEND_FONTSIZE = 15


plot_layout_defaults = {
    'fig_size': (8,6), 
    'tick_labelsize': 18, 
    'ax_spine_thickness': 1.5
}


def plot_layout(**kwargs):

    """
    Set plot layout with invisible top and right axis, and bigger axix thickness and tick sizes. 
    
    Parameters
    -----------
    fig_size: tuple
        gives the x- and y-dimensions of the figure

    ax_spine_thickness: float
        linewidth of the axis spines

    tick_labelsize: float
        fontsize of the axis ticks 
    """

    params = plot_layout_defaults.copy()
    params.update(kwargs)

    fig, ax = plt.subplots(figsize = params['fig_size'])

    ax.spines.right.set_visible(True)
    ax.spines.top.set_visible(True)
    ax.spines.bottom.set_linewidth(params['ax_spine_thickness'])
    ax.spines.left.set_linewidth(params['ax_spine_thickness'])
    ax.spines.top.set_linewidth(params['ax_spine_thickness'])
    ax.spines.right.set_linewidth(params['ax_spine_thickness'])
    plt.tick_params(axis = 'both', which = 'major', labelsize = params['tick_labelsize'])
    pos = ax.get_position()
    ax.set_position([pos.x0, pos.y0 + pos.height * 0.2, pos.width, pos.height * 1])

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox = True, ncol = 5)


# dictionaries to assign colors and markers to the species/dataset manually
species_colors = {
    'Zebrafish': 'green', 
    'Axolotl Dataset 1': 'black',
    'Axolotl Dataset 2': 'slategrey',
    'Dreissena': 'm',
    'Drosophila Study 1': 'blue',
    'Drosophila Study 2': 'dodgerblue',
    'Drosophila Study 3': 'mediumturquoise', 
    'Sea urchin': 'firebrick', 
    'Fundulus YSL': 'limegreen', 
    'C elegans full': 'crimson', 
    'C elegans posterior': 'crimson' , 
    'C elegans p': 'crimson',
    'C elegans p lin': 'crimson',
    'C elegans anterior': 'crimson', 
    'C elengans all fitted together': 'crimson', 
    'Xenopus Study 1': 'mediumpurple',
    'Xenopus Study 2': 'rebeccapurple', 
    'Nematostella': 'darkorange', 
    'Oikoplera': 'red', 
    'Japanese Purple Mussel': 'purple',
    'Killifish': 'red'
}

species_colors_per_species = {
    'Zebrafish': 'green', 
    'Axolotl': 'black',
    'Dreissena': 'm',
    'Drosophila': 'blue',
    'Sea urchin': 'firebrick', 
    'Fundulus': 'limegreen', 
    'C. elegans': 'crimson' , 
    'Xenopus': 'mediumpurple',
    'Nematostella': 'darkorange', 
    'Oikoplera': 'red', 
    'Japanese Purple Mussel': 'purple', 
    'Killifish': 'red'
}

species_markers = {
    'Zebrafish': '^', 
    'Axolotl': 'o',
    'Dreissena': 'd',
    'Drosophila': 'v',
    'Sea urchin': '*', 
    'Fundulus': 'X', 
    'C. elegans': 'h' , 
    'C. elegans p': 'h' , 
    'C. elegans a': 'h' , 
    'Xenopus': 's',
    'Nematostella': 'p', 
    'Oikoplera': 'o', 
    'Japanese Purple Mussel': 'X', 
    'Killifish': 'o'

    }


sg_literature_values = {
    'Zebrafish': 14, 
    'Axolotl': 15.5,
    'Drosophila': 14,
    'C. elegans': 5.5,
    #'C. elegans p': 5, 
    'Xenopus': 15 ,
    'Sea urchin': 9.5, 
    'Nematostella': 12, 
    'Dreissena': 6, 
    'Killifish': 11.5
    #'Oikoplera': 6, 
    #'Japanese Purple Mussel': 5.2

    }

species_full_names =  {
    'Zebrafish': r'$D. rerio$', 
    'Axolotl': r'$A. mexicanum$', 
    'Drosophila': r'$D. melanogaster$', 
    'Sea urchin': r'$T. toreumaticus$', 
    'Xenopus': r'$X. laevis$'
}


save_figures_defaults = {
    'save': True, 
    'dpi': 1200
}

def save_figures(name, **kwargs):
     
     """
     Save the figure under a given name if 'save' variable is set to true either globally (in the defaults dictionary)
     or locally as a parameter of this function --> save_figures(name, save = True)

     Parameters:
     -------------
     save: bool
        saving the figure only if this is set to True, False per default

    dpi: float
        dpi value (image resolution), default = 1200
     """

     params = save_figures_defaults.copy()
     params.update(kwargs)
    
    # only save the image under the given name if the bool 'save' is set to True
     if params['save'] == True:
          plt.savefig(name, dpi = params['dpi'])




species_name_dict = {
    'Zebrafish': 'D. rerio', 
    'Axolotl': 'A. mexicanum', 
    'Drosophila': 'D. melanogaster', 
    'Dreissena': 'D. polymorpha', 
    'C. elegans': 'C. elegans', 
    'Nematostella': 'N. vectensis', 
    'Sea urchin': 'T. toreumaticus', 
    'Xenopus': 'X. laevis'
}
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

convert_lineage_tree_defaults = {
    'lineage': None
}

def convert_lineage_tree(df, gen_name, position_within_generation, time_axis_position, species, **kwargs):
    """Calculate mean and sd of CCL over generation from lineage tree data points 

    Args:
        df (pandas.DataFrame): raw data from a lineage tree data set
        gen_name (str): the column name of the data frame column containing the generation 
        position_within_generation (str): which axis holds information about the position of a cell within the generation? 'x' in vertical trees, 'y' in horizontal trees
        time_axis_position (str): axis on which generations/times are noted -> 'x' for horizontal trees, 'y' for vertical trees
        species (str): species name 

    Returns:
        df (pandas.DataFrame): returns a data frame that shows the mean and sd of CCL for a given generation 
    """    

    params = convert_lineage_tree_defaults.copy()
    params.update(kwargs)

    # first sort the dataframe by generation and by position within the generation (x or y depending on the graph)
    df = df.sort_values(by  = [gen_name, position_within_generation])

    # extract the maximum generation shown in the data - for number of iterations for the next step (calculating duration)
    max_gen = max(df[gen_name])

    # for calculating duration, iterate as many times as there are generations in the dataset and save duration in a list - first entry = 0 
    
    durations = [0]
    for i in range(1, max_gen+1):                       # starts iteration at generation 1         
        
        # define the current cycle as the cycle with the generation being i (current iteration)
        current_cleaveage = df[df[gen_name] == i].reset_index()
        # load the previous cleavage as well 
        previous_cleavage = df[df[gen_name] == i-1].reset_index()


        # now for every enetry in the current cell cycle, substract the time-axis-postition of the 
        # mother cell from the current one to obtain the duration of the cycle    
        for j in range(len(current_cleaveage)):
            # get just the position on the time axis for the current cell and cycle
            current_division_time = current_cleaveage[time_axis_position][j]

            # through the mother cell index, access the position of the mother cell on the time axis 
            mother_cell = current_cleaveage['mother cell index'][j]                     # first identify the mother cell
            last_division_time = previous_cleavage[time_axis_position][mother_cell]     # then its position on the time axis 

            duration = (current_division_time - last_division_time)
            durations.append(float(duration))
    
    
  
    df['duration'] = durations
    df = df[df['cleavage'] > 0]

    # check if there is lineage specified in the function call
    if params['lineage'] != None:
        print('lineage detected')

        if type(params['lineage']) == tuple:
            #print(params['lineage'])
            #print(len(params['lineage']))

            tuple_dfs = []
            for i in range(len(params['lineage'])):
                df_i = df[df['Lineage'] == params['lineage'][i]]
                tuple_dfs.append(df_i)
            df = pd.concat(tuple_dfs)

        else:
            df = df[df['Lineage'] == params['lineage']]

    df = df.groupby(gen_name)['duration'].agg(['mean', 'std']).reset_index()
    
    # fill the other columns of the df and put columns in unified order
    df['generation'] = df[gen_name]
    df['species'] = species
    df['unit'] = 'min'
    df = df.reindex(columns=['species', 'generation', 'mean', 'std', 'unit'])


    return df



def add_SDs (SDa, SDb, SDab):
    return np.sqrt(SDa ** 2 + SDb ** 2 + 2 * SDab)
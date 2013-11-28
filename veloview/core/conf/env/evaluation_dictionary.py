"""This is an example of a combiner description dictionary (expected state dictionary)"""

import veloview.analysis.compfunctions.basic as basic_functions
import veloview.analysis.compfunctions.complex as complex_functions
from veloview.core.conf.env.combiner_description_dictionary import TELL1_NUMBERS, noise_tell1_comb_name_scheme, \
    pedestal_subtracted_hist_name, mean_pedestal_subtracted_hist_name, number_of_clusters_hist_name, \
    active_chip_links_hist_name, cluster_size_hist_name, sensor_occupancy_hist_name, occupancy_spectrum_hist_name, \
    tell1_formatting

# aliases
return_high_score = basic_functions.ReturnAlwaysHighScore


def create_eval_dicts_for_tell1_branch(comb_name_scheme, comp_function):
    return {comb_name_scheme.format(tell1_formatting(number)) : comp_function() for number in TELL1_NUMBERS}


#noinspection PyTypeChecker
def create_eval_dict():
    
    # Noise section
    temp_eval_dict = create_eval_dicts_for_tell1_branch(noise_tell1_comb_name_scheme, 
                                                        return_high_score)
    
    #Crosstalk section
    temp_eval_dict.update({"CrosstalkCombiner" : return_high_score()})
    
    #Pedestals section
    temp_eval_dict.update([ [pedestal_subtracted_hist_name, return_high_score()],
                            [mean_pedestal_subtracted_hist_name, return_high_score()]])
    
    #Clusters section
    temp_eval_dict.update([ [number_of_clusters_hist_name, return_high_score()],
                            [active_chip_links_hist_name, return_high_score()],
                            [cluster_size_hist_name, return_high_score()]])

    #Occupancies section
    temp_eval_dict.update([ [sensor_occupancy_hist_name, return_high_score()],
                            [occupancy_spectrum_hist_name, return_high_score()]])

    return temp_eval_dict

if __name__ == "__main__":
    example_eval_dictionary = create_eval_dict()
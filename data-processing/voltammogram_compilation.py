# this takes a folder of SECCM kinetics data and gets kinetics info from it
# Big note, this is from quasi-reversible analysis.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.ndimage as ndimage
import scipy.constants as constant
import scipy.stats as stats
from scipy.optimize import fsolve
from scipy.optimize import curve_fit
from bard_mirkin_kinetics import get_kinetics2
import os


def main():
    directory = r"G:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\data\24Mar2023_P3HT-with-Fc\scan"
    save_dir = r"G:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\worked-up-data\SECCM_Kinetics\Bard-Mirkin"
    save_name = 'p3ht_results_final'
    settings_name = save_name + "_settings.txt"
    filelist = file_sort(directory)
    linear_region = [0.05, 0.07] # Defining start and end of linear region for background correction
    formal_potential = 0.367 # V, formal redox potential of probe from pt 
    id_potential = 0.1 # V, potential where diffusion-limited current is observed
    diffusion_coef = 4.1 * (10 ** -6) # cm2/s
    tip_radius = 2.7 * (10 **-5) #cm
    potential_range = [0.55, 0.25] # V!
    sweep_number = 1
    sweeps = 3
    goofy_format = False # This is for when the SECCM is configured to record currents in US convention, thus making the potentials backward. Hopefully will be fixed in a future update of the SECCM software.
    show_precalc_plot = True # This will be used to evaluate what parts of the voltammogram will be used in the kinetics evaluation. 
    plotting = False
    

    voltammogram_df = pd.DataFrame()
    
    for filename in filelist:
        count = 0

        if os.path.isfile(os.path.join(directory,filename)):
            data_path = os.path.join(directory,filename)
            
            data = pd.read_csv(data_path, sep='\t')
            data = data_cleanup(data, goofy_format) 
            data['Cleaned Current (pA)'] = current_cleanup(data['Fixed Current (pA)'])
            len_data = len(data)
            cycle_subset = int(len_data / sweeps)
            data_ox_cycle = int(cycle_subset / 2)
            data_subset = data[data_ox_cycle : data_ox_cycle*2].reset_index()
            data_subset = data_subset.loc[data_subset['Voltage (V)'].between(potential_range[1], potential_range[0])]

            zeroed = background_zero(data_subset['Cleaned Current (pA)'])
            max_current = np.max(zeroed)
            normalized = zeroed / max_current
            data_subset['Normalized Current (pA)'] = normalized

            if count == 0:
                voltammogram_df['Potential (V)'] = data_subset['Voltage (V)']
                count += 1

            column_name = filename
            voltammogram_df[filename + " Normalized Current (pA)"] = data_subset['Normalized Current (pA)']
    
            if show_precalc_plot:
                precalc_plot(data, data_subset, -20, 20)
            
            show_precalc_plot = False # only show for the first plot


        else:
            print('skip')

    voltammogram_df.to_csv(r"G:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\worked-up-data\SECCM_Kinetics\Bard-Mirkin\P3HT\p3ht_combined_cleaned_voltammograms.csv")


def file_sort(dir_path):
    data_list = []
    for item in os.listdir(dir_path):
        if item.endswith('.csv'):
            data_list.append(item)
    sorted_file_list = sorted(data_list, key=lambda x: [[int(x.split("_")[1][:-1])], [int(x.split("_")[0][:-1])]])
    # the above is a mouthful. This is sorting based on the X and Y value. lambda x here can be thought of as the item in the list. it is then split at the "_"
    # since this is the separator between the numbers. Indices 0 and 1 are the "numX" and "numY", the [:-1] removes the "X" and "Y" from the string. It's all
    # then converted to an int.
    return sorted_file_list


def data_cleanup(data, goofy_format):
    
    
    if goofy_format:
        print('fill in later')
    
    
    else:
        fixed_current = data['Current (pA)'] * -1
        data['Fixed Current (pA)'] = fixed_current
        
    return data


def precalc_plot(data, data_subset, ylim1, ylim2):
    fig, ax = plt.subplots(1,3, figsize=(10,4))
    ax[0].set_title('Raw Data')
    ax[0].plot(data['Voltage (V)'], data['Fixed Current (pA)'], color='black', alpha=0.3)
    ax[0].plot(data['Voltage (V)'], data['Cleaned Current (pA)'], color='black', alpha=1)
    ax[0].plot(data_subset['Voltage (V)'], data_subset['Cleaned Current (pA)'], color='red', alpha=1)
    
    ax[1].set_title('Subset')
    ax[1].plot(data_subset['Voltage (V)'], data_subset['Cleaned Current (pA)'], color='red', alpha=1)

    ax[2].set_title('Normalized')
    ax[2].plot(data_subset['Voltage (V)'], data_subset['Normalized Current (pA)'], color='blue', alpha=1)

    ax[0].set_ylim(ylim1, ylim2)
    ax[0].set_ylabel("Current (pA)")
    ax[0].set_xlabel('Potential (V)')
    ax[0].invert_xaxis()
    ax[1].invert_xaxis()
    ax[2].invert_xaxis()


    ax[0].set_box_aspect(1)
    ax[1].set_box_aspect(1)
    ax[2].set_box_aspect(1)


    plt.show()


def background_zero(current_data):
    minimum_current = np.min(current_data)
    zeroed_current = current_data - minimum_current
    return zeroed_current


def current_cleanup(current_data):
    sav_gol = signal.savgol_filter(current_data, 10, 3)
    cleaned_current = ndimage.gaussian_filter1d(sav_gol, 15)
    return cleaned_current


if __name__ == "__main__":
    main()
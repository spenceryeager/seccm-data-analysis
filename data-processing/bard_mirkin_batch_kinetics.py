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
    directory = r"E:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\data\28Mar2023_PBTTT_Fc\scan"
    save_dir = r"E:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\worked-up-data\SECCM_Kinetics\Bard-Mirkin"
    save_name = 'pbttt_results.csv'
    settings_name = "settings.txt"
    filelist = file_sort(directory)
    linear_region = [0.05, 0.07] # Defining start and end of linear region for background correction
    formal_potential = 0.4 # V, formal redox potential of probe
    id_potential = 0.1 # V, potential where diffusion-limited current is observed
    diffusion_coef = 4.1 * (10 ** -6) # cm2/s
    tip_radius = 2.7 * (10 **-5) #cm
    potential_range = [0.6, 0.25] # V!
    sweep_number = 1
    sweeps = 3
    goofy_format = False # This is for when the SECCM is configured to record currents in US convention, thus making the potentials backward. Hopefully will be fixed in a future update of the SECCM software.
    show_precalc_plot = True # This will be used to evaluate what parts of the voltammogram will be used in the kinetics evaluation. 
    plotting = False
    
    save_settings(save_dir, settings_name, directory, linear_region, formal_potential, id_potential, diffusion_coef, tip_radius, potential_range, sweep_number)

    # kinetics_df = pd.DataFrame(columns = ['Half Potential (V)', 'Rate Constant (cm/s)', 'log10 Rate Constant', "Transfer Coefficient", "Transfer Coefficient Error", "KappaNaught", "KappaNaught Error", "X (um)", "Y (um)"])
    # half_potential_list = []
    # rate_constant_list = []
    # transfer_coef_list = []
    # transfer_coef_error_list = []
    # kappa_naught_list = []
    # kappa_naught_error_list = []
    quarter_potential = []
    half_potential = []
    three_quarter_potential = []
    delta_quarters = []
    x_list = []
    y_list = []

    kinetics_df = pd.DataFrame(columns=['E1/4 (V)', 'E1/2 (V)', 'E3/4 (V)', 'dE1/4_3/4'])
    
    for filename in filelist:

        if os.path.isfile(os.path.join(directory,filename)):
            split_name = filename.split('_')
            xvals = split_name[0].split("X")
            yvals = split_name[1].split("Y")
            x_list.append(int(xvals[0]))
            y_list.append(int(yvals[0]))
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

    
            if show_precalc_plot:
                precalc_plot(data, data_subset, -20, 20)
            
            show_precalc_plot = False # only show for the first plot

            h, q, tq = get_kinetics2(data_subset=data_subset, plotting=plotting)


            quarter_potential.append(q)
            half_potential.append(h)
            three_quarter_potential.append(tq)
            delta_quarters.append(q-tq)


        else:
            print('skip')


    # kinetics_df['Half Potential (V)'] = half_potential_list
    # kinetics_df['Rate Constant (cm/s)'] = rate_constant_list
    # kinetics_df['log10 Rate Constant'] = np.log10(rate_constant_list)
    # kinetics_df['Transfer Coefficient'] = transfer_coef_list
    # kinetics_df['Transfer Coefficient Error'] = transfer_coef_error_list
    # kinetics_df['KappaNaught'] = kappa_naught_list
    # kinetics_df['KappaNaught Error'] = kappa_naught_error_list
    kinetics_df['E1/4 (V)'] = quarter_potential
    kinetics_df['E1/2 (V)'] = half_potential
    kinetics_df['E3/4 (V)'] = three_quarter_potential
    kinetics_df['dE1/4_3/4'] = delta_quarters
    kinetics_df['X (um)'] = x_list
    kinetics_df['Y (um)'] = y_list
    
    kinetics_df.to_csv(os.path.join(save_dir, save_name))


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


def save_settings(save_dir, settings_name, directory, linear_region, formal_potential, id_potential, diffusion_coef, tip_radius, potential_range, sweep_number):
    settings_file = os.path.join(save_dir, settings_name)
    print(settings_file)
    with open(settings_file, "wt", encoding="utf-8") as file:
        file.write("These settings can be used to replicate the data processing conditions. Input them in the exact location on the batch_kinetics_processing.py file")
        file.write('\n')
        file.write('\n')
        file.write("Data used: " + directory)
        file.write('\n')
        file.write('Linear region selected for background correction: linear_region = '+ str(linear_region))
        file.write('\n')
        file.write('Formal potential of redox probe: formal_potential = ' + str(formal_potential))
        file.write('\n')
        file.write('Location where diffusion limited current occurs: id_potential = ' + str(id_potential))
        file.write('\n')
        file.write('Diffusion coefficient used: diffusion_coef = '+ str(diffusion_coef))
        file.write('\n')
        file.write('Tip radius used: tip_radius = ' + str(tip_radius))
        file.write('\n')
        file.write('Potential range to select the voltammogram from: potential_range = '+ str(potential_range))
        file.write('\n')
        file.write('Sweep number used: sweep_number = ' + str(sweep_number))
        file.close()

if __name__ == "__main__":
    main()
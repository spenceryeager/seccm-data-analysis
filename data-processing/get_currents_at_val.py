import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.ndimage as ndimage
import matplotlib as mpl
import os



def main():
    directory_path = r'/run/media/spencer/My Passport/RDrive_Backup/Spencer Yeager/papers/paper4_pbtttt_p3ht_transfer_kinetics/data/SECCM_Data/02June2026_rrP3HT_Colocation/scan' # this is the directory path that contains the entire SECCM run of interest
    dir_list = file_sort(directory_path) # this is the sorted file list in order of recorded CV / spatially sorted

    ##### Settings to change for analysis #####
    path_to_save = r'/run/media/spencer/My Passport/RDrive_Backup/Spencer Yeager/papers/paper4_pbtttt_p3ht_transfer_kinetics/data/SECCM_Data/02June2026_rrP3HT_Colocation/worked-up-data' # save path
    save_name = "disordered_anodic_currents" # name of the file to save
    save = True # do you want to save your dataframe?
    number_of_scans = 1 # This is the number of FULL scans, i.e. one full cycle.
    visualize_only = False # do you only want to visualize to select a potential?
    visualize_first = True # this will plot the first file in dir_list
    every_val = False # this is for grabbing every value, both oxidation and reduction sweeps.
    oxidation_vals = True # this will obtain values from the oxidation sweep
    oxidation_sweep_first = True # is the oxidation sweep the first sweep of the voltammogram?
    potential_to_grab_ox = 0.937 # this is the potential with which anodic currents values will be grabbed
    potential_to_grab_red = 0 # this is the potential with which cathodic currents will be grabbed
    anodic_current_list = [] # this is the initial empty list that values will be appended to


    if visualize_first:
        visualize(directory_path, dir_list[0], potential_to_grab_ox, potential_to_grab_red)
        
        if visualize_only:
            quit()


    if every_val:
        print('Implementing later')
        file_subset = 0
    else:
        # file_subset = get_subset(directory_path, dir_list[0], number_of_scans, oxidation_sweep_first)
        # get_single_currents(file_subset, potential_to_grab_ox)
        index = 1
        cv_number = len(dir_list)
        for file in dir_list:
            file_subset = get_subset(directory_path, file, number_of_scans, oxidation_sweep_first)
            current_vals = get_single_currents(file_subset, potential_to_grab_ox)
            anodic_current_list.append(current_vals['Cleaned Current (pA)'].iloc[0])
            print('CV ' + str(index) + ' of ' + str(cv_number))
            index += 1

    
    ## SAVING AND DATAFRAME CONSTRUCTION ##
    # this is making the column header name for the dataframe
    if oxidation_vals:
        df_name = 'Anodic Currents at ' + str(potential_to_grab_ox) + "V"
    
    else:
        df_name = 'Cathodic Currents at ' + str(potential_to_grab_ox) + "V"

    # Data frame construction andsave
    data_frame = pd.DataFrame({df_name : anodic_current_list})
    
    if save:
        data_frame.to_csv(os.path.join(path_to_save, save_name + '.csv'))


def get_single_currents(sweep, potential):
    current_val = sweep.iloc[sweep['Voltage (V)'] == potential]
    return current_val


def get_subset(directory_path, file, number_of_scans, oxidation_sweep_first):
    file_load = pd.read_csv(os.path.join(directory_path, file), sep = '\t')
    file_length = len(file_load)
    single_scan_length = int(file_length / number_of_scans)
    sweep_length = int(single_scan_length / 2)


    if oxidation_sweep_first:
        file_subset = file_load[:sweep_length].copy()
        cleaned_up_current = current_fit(file_subset['Current (pA)'])
        file_subset['Cleaned Current (pA)'] = cleaned_up_current
        file_subset.reset_index(drop=True, inplace=True)
    else:
        file_subset = file_load[sweep_length:].copy()
        cleaned_up_current = current_fit(file_subset['Current (pA)'])
        file_subset['Cleaned Current (pA)'] = cleaned_up_current
        file_subset.reset_index(drop=True, inplace=True)


    return file_subset



    
def visualize(directory_path, file, potential_to_grab_ox, potential_to_grab_red):
    voltammogram_load = pd.read_csv(os.path.join(directory_path, file), sep='\t')
    cleaned_up_current = current_fit(voltammogram_load['Current (pA)'])
    voltammogram_load['Cleaned Current (pA)'] = cleaned_up_current
    fig, ax = plt.subplots()
    ax.plot(voltammogram_load['Voltage (V)'], voltammogram_load['Current (pA)'], color='black', alpha=0.5)
    ax.plot(voltammogram_load['Voltage (V)'], voltammogram_load['Cleaned Current (pA)'], color='red', label='Smoothed Current')
    y_vals = ax.get_ylim()
    # Comment either of the below out if you do not want to see them if adding images to data analysis slides.
    ax.vlines(potential_to_grab_ox, y_vals[0], y_vals[1], label=('Anodic Grab: '+str(potential_to_grab_ox) + 'V'), color='green')
    # ax.vlines(potential_to_grab_red, y_vals[0], y_vals[1], label=('Cathodic Grab: ' + str(potential_to_grab_red) + 'V'), color='blue')
    ax.legend(fontsize=10)
    plt.show()


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


def current_fit(current):
    # applying a savitzky golay filter
    savgol_current = signal.savgol_filter(current, 50, 5)
    cleaned_current = ndimage.gaussian_filter1d(savgol_current, 15)
    return cleaned_current


if __name__ == "__main__":
    main()
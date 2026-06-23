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
    visualize_first = True # this will plot the first file in dir_list
    oxidation_vals = True # this will obtain values from the oxidation sweep


    if visualize_first:
        visualize(directory_path, dir_list[0])

    
def visualize(directory_path, file):
    voltammogram_load = pd.read_csv(os.path.join(directory_path, file), sep='\t')
    cleaned_up_current = current_fit(voltammogram_load['Current (pA)'])
    voltammogram_load['Cleaned Current (pA)'] = cleaned_up_current
    fig, ax = plt.subplots()
    ax.plot(voltammogram_load['Voltage (V)'], voltammogram_load['Current (pA)'], color='black', alpha=0.5)
    ax.plot(voltammogram_load['Voltage (V)'], voltammogram_load['Cleaned Current (pA)'], color='red')
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
# this program will grab the maximum current from a chosen potential
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def main():
    get_currents()


def get_currents():
    working_directory = r'dir'
    dir_list = file_sort(working_directory)
    current_list = []

    for path in dir_list:
        current = get_voltage(os.path.join(working_directory, path))
        current_list.append(current)
    
    make_plot(current_list)


def make_plot(current_list):
    font = {'size': 14}
    plt.rc('font', **font)
    sample_size = len(current_list)
    bin_count = int(np.ceil(np.log2(sample_size)) + 1)
    fig, ax = plt.subplots(tight_layout=True)
    ax.hist(current_list, bin_count, edgecolor='black', color='firebrick')
    ax.set_xlabel('Anodic Current (pA)')
    ax.set_ylabel('Counts')
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


def get_voltage(filepath):
    get_oxidation = True
    data = pd.read_csv(filepath, sep='\t')
    data_length = len(data)
    scans = int(data_length / 3)
    # uncomment to get a plot to figure out what points to analyze
    # fig, ax = plt.subplots()
    # ax.plot(data['Voltage (V)'][scans:], data['Current (pA)'][scans:]*-1)
    # ax.invert_xaxis()
    # plt.show()
    V1 = 0.875 # V
    scan_numb = 2
    reduction_scan_start = scan_numb*scans # or multiples of scan
    reduction_scan_end = scan_numb*scans + int(scans/2) # or multiples of scan
    oxidation_scan_start = int((scan_numb * scans)) + int(scans/2) #or multiples of scan
    oxidation_scan_end = int((scan_numb * scans) + scans) # or multiples of scan
    subset = data[oxidation_scan_start:oxidation_scan_end]
    # print(subset)
    val = -1 * subset.loc[subset['Voltage (V)'] == V1, 'Current (pA)'].iloc[0]
    return val
    

if __name__ == "__main__":
    main()
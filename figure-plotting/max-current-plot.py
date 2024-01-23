# this program will grab the maximum current from a chosen potential
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def main():
    get_currents()


def get_currents():
    working_directory = r"\\engr-drive.bluecat.arizona.edu\Research\Ratcliff\Spencer Yeager\data\GATech-Collab-Static-Disorder-In-Polymers\04Jan2024_115kgP3HT_SECCM\scan"
    save_directory = r"\\engr-drive.bluecat.arizona.edu\Research\Ratcliff\Spencer Yeager\papers\paper2_GATech_Collab_P3HT-PBTTT\worked_up_data\histogram\p3ht"
    save_name = "p3ht_crystalline_anodic_current_062V.csv"
    dir_list = file_sort(working_directory)
    number_of_scans = 2
    current_list = []
    potential_to_get = -0.62

    for path in dir_list:
        current = get_voltage(os.path.join(working_directory, path), potential_to_get, number_of_scans)
        current_list.append(current)
    
    current_df = pd.DataFrame(current_list, columns=['Current (pA)'])
    current_df.to_csv(os.path.join(save_directory, save_name))
    # make_plot(current_list)


def make_plot(current_list):
    font = {'size': 14}
    plt.rc('font', **font)
    sample_size = len(current_list)
    bin_count = int(np.ceil(np.log2(sample_size)) + 1)
    fig, axes = plt.subplots()
    axes.hist(current_list, bin_count, edgecolor='royalblue', color='dodgerblue', label='P3HT Crystalline Domain')
    axes.set_xlabel('Anodic Current (pA)')
    axes.set_ylabel('Counts')
    axes.xaxis.set_visible(False)
    plt.subplots_adjust(wspace=0.0,hspace=0.0)
    lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

    fig.legend(lines, labels, fontsize=10, loc=2, bbox_to_anchor=(0.15, 0.85))
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


def get_voltage(filepath, voltage, number_of_scans):
    get_oxidation = True
    data = pd.read_csv(filepath, sep='\t')
    data_length = len(data)
    # print(data_length)
    scans = int(data_length / number_of_scans)
    scan_subset = int(scans / 2)

    # uncomment to get a plot to figure out what points to analyze
    # fig, ax = plt.subplots()
    # ax.plot(data['Voltage (V)'][scans+scan_subset:]*-1, data['Current (pA)'][scans+scan_subset:])
    # ax.invert_xaxis()
    # plt.show()

    subset = data[scans+scan_subset:]
    val = subset.loc[subset['Voltage (V)'] == voltage, 'Current (pA)'].iloc[0]
    return val
    

if __name__ == "__main__":
    main()
# this program will grab the maximum current from a chosen potential
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.stats import norm
from scipy.signal import find_peaks, peak_widths

def main():
    get_currents()


def get_currents():
    working_directory = r"C:\Users\spenceryeager\Documents\seccm-data\22Apr2023_rrP3HT_NoFc\scan"
    working_directory2 = r"C:\Users\spenceryeager\Documents\seccm-data\27Mar2023_PBTTT_NoFc\scan"
    dir_list = file_sort(working_directory)
    dir_list2 = file_sort(working_directory2)
    current_list = []
    current_list2 = []
    current_list3 = []

    for path in dir_list:
        current = get_voltage(os.path.join(working_directory, path), 0.600)
        current_list.append(current)
    
    for path in dir_list:
        current = get_voltage(os.path.join(working_directory, path), 1.04)
        current_list2.append(current)

    for path in dir_list2:
        current = get_voltage(os.path.join(working_directory2, path), 0.8)
        current_list3.append(current)

    make_plot(current_list, current_list2, current_list3)


def make_plot(current_list, current_list2, current_list3):
    mu1, sigma1 = norm.fit(current_list)
    mu2, sigma2 = norm.fit(current_list2)
    mu3, sigma3 = norm.fit(current_list3)
    


    font = {'size': 14}
    plt.rc('font', **font)
    sample_size = len(current_list)
    bin_count = int(np.ceil(np.log2(sample_size)) + 1)
    bin_count2 = int(np.ceil(np.log2(len(current_list3)))+1)

    x1 = np.linspace(-5,-1, 1000)
    y1 = norm.pdf(x1, mu1, sigma1) * 150
    fwhm = 2.355*sigma1
    print(fwhm)

    x2 = np.linspace(-16,-4, 1000)
    y2 = norm.pdf(x2, mu2, sigma2) * 550
    fwhm = 2.355*sigma2
    print(fwhm)

    x3 = np.linspace(-5,-1, 1000)
    y3 = norm.pdf(x3, mu3, sigma3) * 200
    fwhm = 2.355*sigma3
    print(fwhm)

    fig, axes = plt.subplots(2)
    axes[1].hist(current_list, bin_count, edgecolor='white', color='dodgerblue', label='P3HT Crystalline Domain')
    axes[1].plot(x1, y1, color='royalblue', label='P3HT Crystalline Gaussian Fit')

    axes[1].hist(current_list2, bin_count, edgecolor='white', color='steelblue', label='P3HT Amorphous Domain')
    axes[1].plot(x2, y2, color='darkslategray', label='P3HT Amorphous Gaussian Fit')

    axes[0].hist(current_list3, bin_count2, edgecolor='white', color='firebrick', label='PBTTT Amorphous Domain')
    axes[0].plot(x3, y3, color='maroon', label='PBTTT Amorphous Gaussian Fit')
    
    axes[1].set_xlabel('Anodic Current (pA)')
    axes[1].set_ylabel('Counts')
    axes[1].set_xlim(-16,-1)
    axes[0].set_xlim(-16,-1)
    axes[0].xaxis.set_visible(False)
    plt.subplots_adjust(wspace=0.0,hspace=0.0)
    lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

    fig.legend(lines, labels, fontsize=8, loc=2, bbox_to_anchor=(0, 1), ncol=3)
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


def get_voltage(filepath, voltage):
    get_oxidation = True
    data = pd.read_csv(filepath, sep='\t')
    data_length = len(data)
    scans = int(data_length / 3)
    # uncomment to get a plot to figure out what points to analyze
    # fig, ax = plt.subplots()
    # ax.plot(data['Voltage (V)'][scans:], data['Current (pA)'][scans:]*-1)
    # ax.invert_xaxis()
    # plt.show()
    
    scan_numb = 2
    reduction_scan_start = scan_numb*scans # or multiples of scan
    reduction_scan_end = scan_numb*scans + int(scans/2) # or multiples of scan
    oxidation_scan_start = int((scan_numb * scans)) + int(scans/2) #or multiples of scan
    oxidation_scan_end = int((scan_numb * scans) + scans) # or multiples of scan
    subset = data[oxidation_scan_start:oxidation_scan_end]
    # print(subset)
    val = -1 * subset.loc[subset['Voltage (V)'] == voltage, 'Current (pA)'].iloc[0]
    return val
    

if __name__ == "__main__":
    main()
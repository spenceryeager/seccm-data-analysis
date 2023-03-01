# this program will grab the maximum current from a chosen potential
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def main():
    get_currents()


def get_currents():
    working_directory = r"D:\Research\SPECS-Project\2023\15Feb2023_rrP3HT_500nm-tip\scan"
    dir_list = file_sort(working_directory)
    get_voltage(os.path.join(working_directory, dir_list[0]))


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
    data = pd.read_csv(filepath, sep='\t')
    data_length = len(data)
    scans = int(data_length / 3)
    fig, ax = plt.subplots()
    ax.plot(data['Voltage (V)'][scans:], data['Current (pA)'][scans:]*-1)
    ax.invert_xaxis()
    plt.show()

if __name__ == "__main__":
    main()
# this program will grab the maximum current from a chosen potential
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def main():
    get_currents()


def get_currents():
    working_directory = r"dir"
    dir_list = file_sort(working_directory)

    x_list = []
    y_list = []
    for filename in dir_list:
        split_name = filename.split("_")
        x_list.append(int(split_name[0][:-1]))
        y_list.append(int(split_name[1][:-1]))

    unique_x = list(set(x_list))
    unique_y = list(set(y_list))
    X, Y = np.meshgrid(unique_x, unique_y)


    current_list = []

    for path in dir_list:
        current = get_voltage(os.path.join(working_directory, path))
        current_list.append(current)
    
    xy_current = pd.DataFrame(list(zip(x_list, y_list, current_list)), columns = ['X', 'Y', 'Current (pA)'])
    Z_current = xy_current.pivot_table(index="X", columns="Y", values="Current (pA)").T.values

    make_plot(X, Y, Z_current)


def make_plot(X, Y, Z_current):
    font = {'size': 14}
    plt.rc('font', **font)
    fig, ax = plt.subplots(tight_layout=True)
    im = ax.pcolormesh(X, Y, Z_current, vmin=-4.5, vmax=-2.5)
    ax.set_xlabel('X ($\\rm\mu$m)')
    ax.set_ylabel('Y ($\\rm\mu$m)')
    cb = fig.colorbar(im, ax=ax)
    cb.set_label('Current (pA)')
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
    V1 = 1.038 # V
    V2 = 0.760 # V
    subset = data[(scans + int(scans/2)):(scans + 2*int(scans/2))]
    val = -1 * subset.loc[subset['Voltage (V)'] == V2, 'Current (pA)'].iloc[0]
    return val
    

if __name__ == "__main__":
    main()
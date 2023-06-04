# This program will plot the current for each voltage at its corresponding XY value

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def main():
    make_plot()


def make_plot():
    dir_path = r"\\engr-drive.bluecat.arizona.edu\Research\Ratcliff\Spencer Yeager\data\SPECS-Project\2023\23May2023_c16_PBTTT\scan"
    savepath = r"C:\Users\Spencer\Documents\data-analysis\23May2023_c16_PBTTT\frames"
    data_list = file_sort(dir_path)
    x_list = []
    y_list = []
    for filename in data_list:
        split_name = filename.split("_")
        x_list.append(int(split_name[0][:-1]))
        y_list.append(int(split_name[1][:-1]))

    unique_x = list(set(x_list))
    unique_y = list(set(y_list))
    X, Y = np.meshgrid(unique_x, unique_y)

    data_path = os.path.join(dir_path, data_list[1])
    # data = pd.read_csv(data_path, sep='\t')
    loaded_data = []
    for filename in data_list:
        filepath = os.path.join(dir_path, filename)
        data = pd.read_csv(filepath, sep='\t')
        loaded_data.append(data)
    # removing first element because it doesn't have the same number of elements.
    loaded_data.pop(0)
    file_no = len(loaded_data)
    final_index = len(loaded_data[0])
    index = 0
    while index < final_index:
        savename = str(index) + ".png"
        current_list = []
        current_list.append(0)
        for data in loaded_data:
            current_list.append(data['Current (pA)'][index])
        xy_current = pd.DataFrame(list(zip(x_list, y_list, current_list)), columns = ['X', 'Y', 'Current (pA)'])
        Z_current = xy_current.pivot_table(index="X", columns="Y", values="Current (pA)").T.values
        fig, ax = plt.subplots()
        im = ax.pcolormesh(X, Y, Z_current, vmin=3, vmax=-10)
        ax.set_xlabel('X ($\\rm\mu$m)')
        ax.set_ylabel('Y ($\\rm\mu$m)')
        ax.set_title(str(data['Voltage (V)'][index] * -1) + "V")
        cb = fig.colorbar(im, ax=ax)
        cb.set_label('Current (pA)')
        plt.savefig(os.path.join(savepath, savename))
        plt.close()
        print("frame number", index, "of", final_index, "saved")
        index += 1



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


if __name__ == "__main__":
    main()
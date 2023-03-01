# This program will plot the current for each voltage at its corresponding XY value

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def main():
    make_plot()


def make_plot():
    dir_path = r"R:\Spencer Yeager\data\NiOx_Project\2023\01_Jan\30Jan2023_Juan-NiOx-400nm-tip\scan"
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
    data = pd.read_csv(data_path, sep='\t')
    index = len(data)
    file_count = 0
    while file_count <= index:
        current_list = []
        fileskip = 0
        for i in data_list:
            if fileskip == 0:
                current_list.append(0)
                fileskip += 1
            else:
                data_path = os.path.join(dir_path, i)
                data = pd.read_csv(data_path, sep='\t')
                current_list.append(data['Current (pA)'][file_count])
                voltage = str(data['Voltage (V)'][file_count])

        # print(len(current_list))

        xy_current = pd.DataFrame(list(zip(x_list, y_list, current_list)), columns = ['X', 'Y', 'Current (pA)'])
        Z_current = xy_current.pivot_table(index="X", columns="Y", values="Current (pA)").T.values

        fig, ax = plt.subplots()
        im = ax.pcolormesh(X, Y, Z_current, vmin=-120, vmax=100)
        ax.set_xlabel('X ($\\rm\mu$m)')
        ax.set_ylabel('Y ($\\rm\mu$m)')
        ax.set_title(voltage)
        cb = fig.colorbar(im, ax=ax)
        cb.set_label('Current (pA)')
        savepath = r"C:\Users\spenceryeager\Documents\group_meetings\8Feb2023\400nm-tip\video"
        savename = str(file_count) + ".png"
        plt.savefig(os.path.join(savepath, savename))
        file_count += 100



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
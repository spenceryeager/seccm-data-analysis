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

    # with sorted list, we must read each file and plot it. Have mercy on my computer memory


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
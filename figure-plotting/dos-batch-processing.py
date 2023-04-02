# batch file for calculating DOS from all SECCM runs.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from dos_calculation import dos_array_return
from directory_sorting import directory_sort


def main():
    # fill this area out first
    data_directory = r"C:\Users\spenceryeager\Documents\seccm-data\19Mar2023_rrP3HT_500nm-tip\scan1"
    fc_correction = 0 # how much do we need to adjust the potential based on Fc redox potential?
    sweeps = 3 # how many sweeps are there? this helps with determining sweep cutoffs
    pipette_diameter = 500 # enter this value as nm. It will be converted later
    film_thickness = 27 # enter as nm. 27 nm is an approximation for now.
    v = 0.1 # V/s, scan rate.
    lin_start = -0.15 # this is the linear region start. This region is used to calculate and correct the background
    lin_end = 0.2 # this is the linear region end. This region is used to calculate and correct the background



    file_list = []
    sorted_file_list = directory_sort(data_directory)
    dos_array = np.zeros(len(sorted_file_list))
    index = 0
    fig, ax = plt.subplots()
    for filepath in sorted_file_list:
        dos, data_subset = dos_array_return(filepath, fc_correction, sweeps, pipette_diameter, film_thickness, v, lin_start, lin_end)
        #  dos_array[index] = dos
        ax.plot(dos, data_subset['Voltage (V)'], color='red', alpha=0.1)
        index += 1
        #  print(data_subset.head())
    ax.invert_yaxis()
    plt.show()



if __name__ == "__main__":
    main()

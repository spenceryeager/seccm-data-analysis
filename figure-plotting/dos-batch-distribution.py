# batch file for calculating DOS from all SECCM runs.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from dos_calculation import dos_array_return
from directory_sorting import directory_sort


def main():
    # fill this area out first
    data_directory = r"D:\Research\SPECS-Project\2023\22Apr2023_rrP3HT_NoFc\scan"
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

    all_dos_vals = []
    for filepath in sorted_file_list:
        dos, data_subset = dos_array_return(filepath, fc_correction, sweeps, pipette_diameter, film_thickness, v, lin_start, lin_end)
        #  dos_array[index] = dos
        all_dos_vals.append(dos)
        #  print(data_subset.head())
    
    loop_it = len(all_dos_vals)
    val_it = len(all_dos_vals[0])
    i = 0 # i and j are just loop iteration values
    j = 0
    avg_dos = []
    std_dos = []
    while i < loop_it:
        val_calcs = []
        while j < val_it:
            for sub in all_dos_vals:
                val_calcs.append(sub[j])
            avg_dos.append(np.average(val_calcs))
            std_dos.append(np.std(val_calcs))
            j += 1
        i += 1
    print(avg_dos)      
    fig, ax = plt.subplots()
    ax.plot(avg_dos, data_subset['Voltage (V)'], color='red')
    ax.invert_yaxis()
    ax.set_ylim(1.2, 0)

    plt.show() 


if __name__ == "__main__":
    main()

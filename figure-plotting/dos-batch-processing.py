# batch file for calculating DOS from all SECCM runs.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from dos_calculation import dos_array_return
from directory_sorting import directory_sort


def main():
    # Setting font size before making plot
    font = {'size': 12}
    plt.rc('font', **font)
    # fill this area out first
    data_directory = r"C:\Users\Spencer\Documents\test-seccm-data\scan"
    save_data_directory = r"C:\Users\Spencer\Documents\test-seccm-data\dos"
    save_data_name = "pbttt_c16"
    fc_correction = 0 # how much do we need to adjust the potential based on Fc redox potential?
    sweeps = 3 # how many sweeps are there? this helps with determining sweep cutoffs
    pipette_diameter = 500 # enter this value as nm. It will be converted later
    film_thickness = 300 # enter as nm
    v = 0.1 # V/s, scan rate.
    lin_start = 0.15 # this is the linear region start. This region is used to calculate and correct the background
    lin_end = -0.2 # this is the linear region end. This region is used to calculate and correct the background



    file_list = []
    sorted_file_list = directory_sort(data_directory)
    dos_list = []
    index = 0
    fig, ax = plt.subplots()

    dos_df = pd.DataFrame()
    
    for filepath in sorted_file_list:
        dos, data_subset = dos_array_return(filepath, fc_correction, sweeps, pipette_diameter, film_thickness, v, lin_start, lin_end)
        dos_list.append(dos)
        ax.plot(dos, data_subset['Voltage (V)'] * -1, color='blue', alpha=0.1)
        if index == 0:
            dos_df['Potential (V)'] = data_subset['Voltage (V)']
            dos_df[str(index)] = pd.Series(dos)
            index += 1
        else:
            dos_df[str(index)] = pd.Series(dos)
            index += 1
        #  print(data_subset.head())

    # Creating DOS file + estimation information file
    dos_df.to_csv(os.path.join(save_data_directory, save_data_name + ".csv"))
    readme = open(os.path.join(save_data_directory, save_data_name + "_calculation_parameters" ".txt"), 'w')
    readme.write("Analysis code written by Spencer Yeager, University of Arizona \n")
    readme.write("Find the source code here: https://github.com/spenceryeager/seccm-data-analysis/blob/main/figure-plotting/dos-batch-processing.py \n")
    readme.write("Data used: " + data_directory + "\n")
    readme.write("Parameters used to generate this data: \n")
    readme.write("Pipette diameter used = " + str(pipette_diameter) +"\n" )
    readme.write("Film Thickness (nm) = " + str(film_thickness) + "\n")
    readme.write("Scan rate (V/s) = " + str(v) + "\n")
    readme.write("Sweeps = " + str(sweeps) + "\n")
    readme.write("Region used for linear correction (V): " + str(lin_start) + " - " + str(lin_end))
    readme.close()


    # Plotting to ensure everything looks okay
    ax.set_title("Verify plot looks okay")
    ax.set_xlabel("Density of States (eV$^{-1}$ cm$^{-3}$)")
    ax.set_ylabel("Potential (V) vs. Ag/AgCl")
    ax.invert_yaxis()
    ax.minorticks_on()
    potential_limits = ax.get_ylim()
    ax2 = ax.twinx()
    ax2.minorticks_on()
    ax2.set_ylim((potential_limits[0] + 4.5) * -1, (potential_limits[1] + 4.5) * -1)
    ax2.set_ylabel("Energy vs. Vacuum (eV)")
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()

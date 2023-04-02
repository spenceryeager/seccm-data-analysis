# Obtaining density of states from SECCM data

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.signal as signal
import scipy.ndimage as ndimage
import scipy.constants as constant
import scipy.stats as stats


def main():
    plt.rcParams['font.size'] = 14

    # fill this section out beforehand
    fc_correction = 0 # how much do we need to adjust the potential based on Fc redox potential?
    sweeps = 3 # how many sweeps are there? this helps with determining sweep cutoffs
    pipette_diameter = 500 # enter this value as nm. It will be converted later
    film_thickness = 27 # enter as nm. 27 nm is an approximation for now.
    v = 0.1 # V/s, scan rate.
    lin_start = -0.15 # this is the linear region start. This region is used to calculate and correct the background
    lin_end = 0.2 # this is the linear region end. This region is used to calculate and correct the background
    
    filepath = r"file"
    dos, data_subset = dos_array_return(filepath, fc_correction, sweeps, pipette_diameter, film_thickness, v, lin_start, lin_end)
    # this section is for visualizing the current used in the approximation
    # fig, ax = plt.subplots(tight_layout=True)
    # ax.plot(data_subset['Voltage (V)'], corrected_current, color='purple', linewidth=3)
    # ax.invert_xaxis()
    # ax.set_xlabel("Potential (V) vs. Ag/AgCl")
    # ax.set_ylabel("Current (pA)")
    # plt.show()

    # this is the actual DOS plotting area. Removed for now while I mess around
    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(dos / (10 **23), data_subset['Voltage (V)'], color='red', linewidth=3)
    ax.invert_yaxis()
    ax.set_ylim(1.4, 0)
    ax.set_xlim(0)
    ax.minorticks_on()
    ax.set_ylabel("Potential (V) vs. Ag/AgCl")
    ax.set_xlabel("Density of States (eV$^{-1}$ cm$^{-3}$) $\\times$10$^{23}$")
    plt.show()


def dos_array_return(filepath, fc_correction, sweeps, pipette_diameter, film_thickness, v, lin_start, lin_end):
    datafile = pd.read_csv(filepath, sep='\t')
    data_subset = ox_subset(sweeps, datafile, 5)
    cleaned_current = current_cleanup(data_subset['Current (pA)'])
    # print(cleaned_current)
    corrected_current = background_correction(data_subset, cleaned_current, lin_start, lin_end)
    dos = dos_calc(data_subset['Voltage (V)'], corrected_current, pipette_diameter, film_thickness, v)
    return dos, data_subset

def background_correction(data_subset, cleaned_current, lin_start, lin_end):
    # data_subset = data_subset.reset_index(drop=True)
    lin_start_index = data_subset.loc[data_subset['Voltage (V)'] == lin_start].index[0]
    lin_end_index = data_subset.loc[data_subset['Voltage (V)'] == lin_end].index[0]
    lin_regression = stats.linregress(data_subset['Voltage (V)'][lin_start_index:lin_end_index], cleaned_current[lin_start_index:lin_end_index])
    background = (lin_regression[0] * data_subset['Voltage (V)']) + lin_regression[1]
    correction_vals = np.zeros(len(background))
    index = 0
    for val in background:
        correction_vals[index] = (0 - val)
        index += 1
    # print(correction_vals)
    corrected_current = cleaned_current + correction_vals
    return(corrected_current)


def dos_calc(potential, cleaned_current, pipette_diameter, film_thickness, v):
    area = constant.pi * ((pipette_diameter * (10 **-7)) / 2) ** 2
    dos = (cleaned_current * (10**-12)) / area
    dos = dos / (v * (27 * (10 **-7)))
    dos = dos / (constant.elementary_charge ** 2)
    dos = dos * constant.physical_constants['electron volt'][0]
    dos = np.absolute(dos)
    return dos


def ox_subset(sweeps, datafile, start_index):
    sweep_segments = int(len(datafile)/sweeps)
    # in this case, I'll be using sweep 2's oxidation step.
    ox_start = sweep_segments + int(sweep_segments/2)
    ox_end = sweep_segments*2
    datafile = datafile[ox_start:ox_end]
    # print(datafile)
    datafile = datafile[start_index:].reset_index(drop=True)
    return datafile


def current_cleanup(current_data):
    sav_gol = signal.savgol_filter(current_data, 10, 3)
    gauss_current = ndimage.gaussian_filter1d(sav_gol, 20)
    cleaned_current = np.negative(gauss_current)
    return cleaned_current


if __name__ == "__main__":
    main()
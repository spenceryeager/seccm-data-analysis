# Obtaining density of states from SECCM data

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.signal as signal
import scipy.ndimage as ndimage
import scipy.constants as constant


def main():
    plt.rcParams['font.size'] = 14

    # fill this section out beforehand
    fc_correction = 0 # how much do we need to adjust the potential based on Fc redox potential?
    sweeps = 3 # how many sweeps are there? this helps with determining sweep cutoffs
    pipette_diameter = 500 # enter this value as nm. It will be converted later
    film_thickness = 27 # enter as nm. 27 nm is an approximation for now.
    v = 0.1 # V/s, scan rate. 
    

    filepath = r"file"
    datafile = pd.read_csv(filepath, sep='\t')
    data_subset = ox_subset(sweeps, datafile)
    cleaned_current = current_cleanup(data_subset['Current (pA)'][5:])
    dos = dos_calc(data_subset['Voltage (V)'][5:], cleaned_current, pipette_diameter, film_thickness, v)
    # fig, ax = plt.subplots(tight_layout=True)
    # ax.plot(data_subset['Voltage (V)'][5:], data_subset['Current (pA)'][5:] * -1, color='red', alpha=0.2, linewidth=3)
    # ax.plot(data_subset['Voltage (V)'][5:], cleaned_current * -1, color='red', linewidth=3)
    # ax.invert_xaxis()
    # ax.set_xlabel("Potential (V) vs. Ag/AgCl")
    # ax.set_ylabel("Current (pA)")
    # plt.show()

    fig, ax = plt.subplots(tight_layout=True)
    ax.plot(dos / (10 **23), data_subset['Voltage (V)'][5:], color='red', linewidth=3)
    ax.invert_yaxis()
    ax.set_ylim(1.4, 0)
    ax.minorticks_on()
    ax.set_ylabel("Potential (V) vs. Ag/AgCl")
    ax.set_xlabel("Density of States (eV$^{-1}$ cm$^{-3}$) $\\times$10$^{23}$")
    plt.show()


def dos_calc(potential, cleaned_current, pipette_diameter, film_thickness, v):
    area = constant.pi * ((pipette_diameter * (10 **-7)) / 2) ** 2
    dos = (cleaned_current * (10**-12)) / area
    dos = dos / (v * (27 * (10 **-7)))
    dos = dos / (constant.elementary_charge ** 2)
    dos = dos * constant.physical_constants['electron volt'][0]
    dos = np.absolute(dos)
    return dos





def ox_subset(sweeps, datafile):
    sweep_segments = int(len(datafile)/sweeps)
    # in this case, I'll be using sweep 2's oxidation step.
    ox_start = sweep_segments + int(sweep_segments/2)
    ox_end = sweep_segments*2
    return datafile[ox_start:ox_end]


def current_cleanup(current_data):
    sav_gol = signal.savgol_filter(current_data, 10, 3)
    gauss_current = ndimage.gaussian_filter1d(sav_gol, 20)
    cleaned_current = gauss_current
    return cleaned_current


if __name__ == "__main__":
    main()
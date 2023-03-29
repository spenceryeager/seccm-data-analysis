# Obtaining density of states from SECCM data

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.signal as signal
import scipy.ndimage as ndimage


def main():
    dos_calculation()


def dos_calculation():
    plt.rcParams['font.size'] = 20

    # fill this section out beforehand
    fc_correction = 0 # how much do we need to adjust the potential based on Fc redox potential?
    sweeps = 3 # how many sweeps are there? this helps with determining sweep cutoffs
    pipette_diameter = 500 # enter this value as nm. It will be converted later
    film_thickness = 27 # enter as nm. 27 nm is an approximation for now.
    

    filepath = r"file"
    datafile = pd.read_csv(filepath, sep='\t')
    data_subset = ox_subset(sweeps, datafile)
    cleaned_current = current_cleanup(data_subset['Current (pA)'][5:])

    fig, ax = plt.subplots()
    ax.plot(data_subset['Voltage (V)'][5:], data_subset['Current (pA)'][5:] * -1, color='red', alpha=0.2)
    ax.plot(data_subset['Voltage (V)'][5:], cleaned_current * -1, color='red')
    ax.invert_xaxis()
    ax.set_xlabel("Potential (V) vs. Ag/AgCl")
    ax.set_ylabel("Current (pA)")
    plt.show()



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
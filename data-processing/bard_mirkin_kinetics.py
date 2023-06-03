# this will be used to iterate over all recorded CVs and extract kinetics parameters, such as transfer coefficients and rate constants.
# this is adopted from https://doi.org/10.1021/ac00043a020, which is not applicable to semiconductors. But can be used as an approximation
# this biggest assumption baked into this approximation is the electron transfer follows Butler Volmer kinetics.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.signal as signal
import scipy.ndimage as ndimage
import scipy.constants as constant
import scipy.stats as stats

def main():
    # Fill this section out! Future implementation will have a popup box perhaps.
    lin_start = 0.15 # Defining start of linear region for background correction
    lin_end = 0.25 # Defining end of linear region for background correction
    formal_potential = 0.4 # V, formal redox potential of probe
    id_potential = 0.55 # V, potential where diffusion-limited current is observed

    # working parts of code
    plt.rcParams['font.size'] = 14
    data_path = r"data-processing\sample_file\sample_data.csv"
    data = pd.read_csv(data_path, sep='\t')
    length = len(data)
    ox_start = int(length/3)
    ox_end = ox_start + int(ox_start/2)
    ox_start = ox_start + 10
    data = data[ox_start:ox_end]
    cleaned_current = current_cleanup(data['Current (pA)'])
    corrected_current = background_zero(cleaned_current)
    # corrected_current = background_correction(data, cleaned_current, lin_start, lin_end) # deprecated way of correcting current. Skews the trend in my opinion.
    data['Zeroed Current (pA)'] = corrected_current
    data = data.reset_index(drop=True)

    data = get_id(id_potential, data)
    fig, ax = plt.subplots()
    # ax.plot(data['Voltage (V)'], cleaned_current, color='red', label='Uncorrected')
    # ax.plot(data['Voltage (V)'], corrected_current, color='blue', label='Background corrected')
    ax.plot(data['Voltage (V)'], data['Normalized Current (pA)'], color='purple', label='Normalized')

    ax.set_xlabel("Potential (V) vs. AgCl")
    ax.set_ylabel("Current (pA)")
    ax.legend(loc = "upper left", fontsize = 12)
    plt.show()


def current_cleanup(current_data):
    sav_gol = signal.savgol_filter(current_data, 10, 3)
    cleaned_current = ndimage.gaussian_filter1d(sav_gol, 15)
    return cleaned_current


def background_correction(data_subset, cleaned_current, lin_start, lin_end):
    data_subset = data_subset.reset_index(drop=True)
    lin_start_index = data_subset.loc[data_subset['Voltage (V)'] == lin_start].index[0]
    lin_end_index = data_subset.loc[data_subset['Voltage (V)'] == lin_end].index[0]
    # print(cleaned_current[lin_end_index:lin_start_index])
    lin_regression = stats.linregress(data_subset['Voltage (V)'][lin_end_index:lin_start_index], cleaned_current[lin_end_index:lin_start_index])
    background = (lin_regression[0] * data_subset['Voltage (V)']) + lin_regression[1]
    correction_vals = np.zeros(len(background))
    index = 0
    for val in background:
        correction_vals[index] = (0 - val)
        index += 1
    # print(correction_vals)
    corrected_current = cleaned_current + correction_vals
    return(corrected_current)


def background_zero(current_data):
    minimum_current = np.min(current_data)
    zeroed_current = current_data - minimum_current
    return zeroed_current


def get_id(id_potential, data):
    id_val = data.loc[data['Voltage (V)'] == 0.55, 'Zeroed Current (pA)']
    id_current = data['Zeroed Current (pA)'] / id_val.values[0]
    data['Normalized Current (pA)'] = id_current
    return(data)



if __name__ == "__main__":
    main()
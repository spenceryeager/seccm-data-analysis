# this will be used to iterate over all recorded CVs and extract kinetics parameters, such as transfer coefficients and rate constants.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.signal as signal
import scipy.ndimage as ndimage
import scipy.constants as constant
import scipy.stats as stats

def main():
    data_path = r"C:\Users\spenceryeager\Documents\seccm-data\18Feb2023_rrP3HT_500nm-tip-Fc\scan\0X_2Y_rrP3HT-Fc.csv"
    data = pd.read_csv(data_path, sep='\t')
    length = len(data)
    ox_start = int(length/3)
    ox_end = ox_start + int(ox_start/2)
    ox_start = ox_start + 10
    lin_start = 0.15
    lin_end = 0.25
    data = data[ox_start:ox_end]
    cleaned_current = current_cleanup(data['Current (pA)'])
    # print(data)
    corrected_current = background_correction(data, cleaned_current, lin_start, lin_end)

    fig, ax = plt.subplots()
    ax.plot(data['Voltage (V)'], cleaned_current, color='red', label='Uncorrected')
    ax.plot(data['Voltage (V)'], corrected_current, color='blue', label='Background corrected')

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

if __name__ == "__main__":
    main()
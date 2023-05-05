# this will be used to iterate over all recorded CVs and extract kinetics parameters, such as transfer coefficients and rate constants.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.signal as signal
import scipy.ndimage as ndimage
import scipy.constants as constant
import scipy.stats as stats

def main():
    data_path = r"D:\Research\SPECS-Project\2023\18Feb2023_rrP3HT_500nm-tip-Fc\scan\0X_2Y_rrP3HT-Fc.csv"
    data = pd.read_csv(data_path, sep='\t')
    length = len(data)
    ox_start = int(length/3)
    ox_end = ox_start + int(ox_start/2)
    ox_start = ox_start + 10
    lin_start = 0.15
    lin_end = 0.25
    cleaned_current = current_cleanup(data['Current (pA)'][ox_start:ox_end])
    print(data[ox_start:ox_end])
    # corrected_current = background_correction(data['Voltage (V)'][ox_start:ox_end], cleaned_current, lin_start, lin_end)

    # fig, ax = plt.subplots()
    # ax.plot(data['Voltage (V)'][ox_start:ox_end], cleaned_current, color='red')
    # ax.plot(data['Voltage (V)'][ox_start:ox_end], corrected_current, color='blue')

    # plt.show()


def current_cleanup(current_data):
    sav_gol = signal.savgol_filter(current_data, 10, 3)
    cleaned_current = ndimage.gaussian_filter1d(sav_gol, 15)
    return cleaned_current


def background_correction(data_subset, cleaned_current, lin_start, lin_end):
    # data_subset = data_subset.reset_index(drop=True)
    print(data_subset)
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


if __name__ == "__main__":
    main()
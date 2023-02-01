# This program will plot a single SECCM CV

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp
import scipy.signal as signal


def main():
    fit_data()


def fit_data():
    # set figure font sizes
    plt.rcParams['font.size'] = 20
    # fit data?
    fit = True

    data_file = r"dir"
    data_read = pd.read_csv(data_file, sep='\t')

    # removing the first approach scan by dividing the length by # of sweeps and starting after the first sweep
    sweeps = 3
    sweep_intervals = int(len(data_read) / sweeps)
    data_subset = data_read[sweep_intervals:]

    fig, ax = plt.subplots(figsize=(8,6))
    if fit == True:
        ax.plot(data_subset["Voltage (V)"], data_subset["Current (pA)"] * -1, color='red', alpha=0.2, label="Raw Current")
        fitted_current  = current_fit(data_subset['Current (pA)'])
        ax.plot(data_subset["Voltage (V)"], fitted_current * -1, color='red', alpha=1, label="Savitzky-Golay Current")
        ax.legend(prop={'size': 16})
    else:
        ax.plot(data_subset["Voltage (V)"], data_subset["Current (pA)"] * -1, color='red', alpha=1)

    ax.invert_xaxis()
    ax.set_ylabel("Current (pA)")
    ax.set_xlabel("Potential vs. Ag Wire (V)")
    plt.tight_layout()
    plt.show()


def current_fit(current):
    # applying a savitzky golay filter
    savgol_current = signal.savgol_filter(current, 50, 5)
    print(savgol_current)
    return savgol_current


if __name__ == "__main__":
    main()
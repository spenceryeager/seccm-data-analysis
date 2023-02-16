# This program will plot two separate SECCM CVs

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

    data_file1 = r"file1"
    data_read1 = pd.read_csv(data_file1, sep='\t')
    data1_label = "PBTTT"

    data_file2 = r"file2"
    data_read2 = pd.read_csv(data_file2, sep='\t')
    data2_label = "rrP3HT"

    # removing the first approach scan by dividing the length by # of sweeps and starting after the first sweep
    sweeps = 3
    sweep_intervals1 = int(len(data_read1) / sweeps)
    data_subset1 = data_read1[sweep_intervals1:]

    sweep_intervals2 = int(len(data_read1) / sweeps)
    data_subset2 = data_read2[sweep_intervals2:]

    fig, ax = plt.subplots(figsize=(8,6))

    ax.plot(data_subset1["Voltage (V)"], data_subset1["Current (pA)"] * -1, color='red', alpha=1, label=data1_label)
    ax.plot(data_subset2["Voltage (V)"], data_subset2["Current (pA)"] * -1, color='blue', alpha=1, label=data2_label)

    ax.invert_xaxis()
    ax.set_ylabel("Current (pA)")
    ax.set_xlabel("Potential vs. Ag/AgCl")
    ax.legend()
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()
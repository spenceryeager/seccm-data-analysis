# This program will plot a single SECCM CV

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp
import scipy.signal as signal
import matplotlib as mpl
from matplotlib import rcParams
import os
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'
rcParams['savefig.dpi'] = 300


def main():
    fit_data()


def fit_data():
    # set figure font sizes
    plt.rcParams['font.size'] = 20
    # fit data?
    fit = False
    reference_label = "Potential (V) vs. Ag Wire"

    data_file = r"G:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\data\28Mar2023_PBTTT_Fc\scan\0X_0Y_pbttt_fc.csv"
    save_dir = r"R:\Spencer Yeager\data\NiOx_Project\2023\09_Sep\20Sep2023_ButtonPtCel\figures"
    save_name = "fc_approach.svg"
    data_read = pd.read_csv(data_file, sep='\t')
    

    # removing the first approach scan by dividing the length by # of sweeps and starting after the first sweep
    sweeps = 2
    sweep_intervals = int(len(data_read) / sweeps)
    data_subset = data_read[sweep_intervals:sweep_intervals*2]
    
    fontsize = 40
    mpl.rcParams.update({'font.size': fontsize, 'figure.autolayout': True})
    fig, ax = plt.subplots(figsize=(14,10), tight_layout=True)
    if fit == True:
        ax.plot(data_subset["Voltage (V)"], data_subset["Current (pA)"] * -1, color='black', alpha=0.2, label="Raw Current")
        fitted_current  = current_fit(data_subset['Current (pA)'])
        ax.plot(data_subset["Voltage (V)"], fitted_current * -1, color='black', alpha=1, label="Savitzky-Golay Current")
        ax.legend(prop={'size': 16})
    else:
        ax.plot(data_subset["Voltage (V)"], data_subset["Current (pA)"] * -1, color='black', alpha=1, linewidth=7)

    ax.invert_xaxis()
    ax.set_ylabel("Current (pA)")
    ax.set_xlabel(reference_label)
    ax.xaxis.labelpad = 5
    ax.yaxis.labelpad = 5
    ax.tick_params(axis = 'both', direction='in', which='both', length=18, width=3)
    
    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3)
    
    # plt.savefig(os.path.join(save_dir, save_name))
    plt.show()


def current_fit(current):
    # applying a savitzky golay filter
    savgol_current = signal.savgol_filter(current, 50, 5)
    print(savgol_current)
    return savgol_current


if __name__ == "__main__":
    main()
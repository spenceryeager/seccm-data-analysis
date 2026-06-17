# This program will plot a single SECCM CV

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp
import scipy.signal as signal
import scipy.ndimage as ndimage
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
    # smooth data?
    fit = True
    # IUPAC format?
    iupac = False
    reference_label = "Potential (V) vs. Ag Wire"

    data_file = r"G:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\data\SECCM_Data\02June2026_rrP3HT_Colocation\reference_calibration\reference_before_5.csv"
    save_name = "fc_approach.svg"
    data_read = pd.read_csv(data_file, sep='\t')
    
    
    if not iupac:
        data_read['Current (pA)'] = np.negative(data_read['Current (pA)'].copy())

        

    fontsize = 25
    mpl.rcParams.update({'font.size': fontsize, 'figure.autolayout': True})
    fig, ax = plt.subplots(figsize=(8,8), tight_layout=True)
    if fit == True:
        ax.plot(data_read["Voltage (V)"], data_read["Current (pA)"], color='black', alpha=0.2, label="Raw Current", linewidth=7)
        fitted_current  = current_fit(data_read['Current (pA)'])
        ax.plot(data_read["Voltage (V)"], fitted_current, color='black', alpha=1, label="Smoothed Current", linewidth=7)
        ax.legend(prop={'size': 16})
    else:
        ax.plot(data_read["Voltage (V)"], data_read["Current (pA)"], color='black', alpha=1, linewidth=7)

    ax.invert_xaxis()
    ax.set_ylabel("Current (pA)")
    ax.set_xlabel(reference_label)
    ax.xaxis.labelpad = 5
    ax.yaxis.labelpad = 5
    ax.minorticks_on()
    ax.tick_params(axis = 'both', direction='in', which='major', length=9, width=3)
    ax.tick_params(axis = 'both', direction='in', which='minor', length=4.5, width=3)

    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3)
    
    # plt.savefig(os.path.join(save_dir, save_name))
    ax.set_box_aspect
    plt.show()


def current_fit(current):
    # applying a savitzky golay filter
    savgol_current = signal.savgol_filter(current, 50, 5)
    cleaned_current = ndimage.gaussian_filter1d(savgol_current, 15)
    return cleaned_current


if __name__ == "__main__":
    main()
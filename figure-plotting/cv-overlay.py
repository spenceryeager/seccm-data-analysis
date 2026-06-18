# Overlay of all CVs collected with 'n =' displayed as a legend.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import scipy as sp
import scipy.signal as signal
import scipy.ndimage as ndimage
import matplotlib as mpl
from matplotlib import rcParams
from matplotlib.lines import Line2D
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'
rcParams['savefig.dpi'] = 300


def main():
    ##############################
    #change these parameters #####
    ##############################
    directory = r"E:\SECCMComputerBackup\CDrive\Data\Spencer\03June2026_rrP3HT_colocation\Fc\scan"
    savefig_directory = r"enter directory to save figure"
    savefig_name = "save_fig_name"
    sweep_numbers = 2 # currently does not do anything
    fc_calibration = 0 # only use this if you want to calibrate X axis to a redox probe
    fc_ev = -4.9
    reference = "Potential (V) vs Ag Wire" # this will be the X axis in the plot
    ev_axis = False # currently does not do anything
    save = True
    us_convention = True
    color = "#e31a1c"
    ##############################
    make_plot(directory, savefig_name, savefig_directory, sweep_numbers, fc_calibration, fc_ev, reference, ev_axis, save, us_convention, color)


def make_plot(directory, savefig_name, savefig_directory, sweep_numbers, fc_calibration, fc_ev, reference, ev_axis, save, us_convention, color):
    
    
    def current_cleanup(current_data):
        sav_gol = signal.savgol_filter(current_data, 10, 3)
        gauss_current = ndimage.gaussian_filter1d(sav_gol, 20)
        return gauss_current

    

    def file_sort(dir_path):
        data_list = []
        for item in os.listdir(dir_path):
            if item.endswith('.csv'):
                data_list.append(item)
        sorted_file_list = sorted(data_list, key=lambda x: [[int(x.split("_")[1][:-1])], [int(x.split("_")[0][:-1])]])
        # the above is a mouthful. This is sorting based on the X and Y value. lambda x here can be thought of as the item in the list. it is then split at the "_"
        # since this is the separator between the numbers. Indices 0 and 1 are the "numX" and "numY", the [:-1] removes the "X" and "Y" from the string. It's all
        # then converted to an int.
        return sorted_file_list

    # File stuff
    # file_list = os.listdir(directory)
    file_list = file_sort(directory)
    v = 'Voltage (V)'
    i = 'Current (pA)'


    # Setting font size before making plot
    fontsize = 40
    mpl.rcParams.update({'font.size': fontsize, 'figure.autolayout': True})

    # creating plot
    fontsize = 40
    mpl.rcParams.update({'font.size': fontsize, 'figure.autolayout': True})
    fig, ax = plt.subplots(figsize=(14,10), tight_layout=True)
    cv_count = 0


    # Creating a color gradient to help distinguish where certain CVs
    cmap_viri = plt.get_cmap('viridis')(np.linspace(0,1,len(file_list)))
    alpha = 0.1
    color_count = 0

    for file in file_list:


        if file.endswith('.csv'):
            cv_count += 1
            data = pd.read_csv(os.path.join(directory, file), sep='\t') # loading in data

            smoothed_current = current_cleanup(data[i])
            # ax.plot(np.negative(data[v][second_sweep:] - fc_calibration), data[i][second_sweep:], color=color, alpha=0.05)

            if us_convention:
                ax.plot(data[v] - fc_calibration, np.negative(smoothed_current), color=cmap_viri[color_count], alpha=alpha, linewidth=3)

            else:
                ax.plot(data[v]  - fc_calibration, smoothed_current, color=cmap_viri[color_count], alpha=alpha, linewidth=3)


            color_count += 1


    if us_convention:
        ax.invert_xaxis()
    #################################
    ###### Formatting plot ##########
    ax.minorticks_on()
    ax.set_xlabel(reference)
    ax.set_ylabel("Current (pA)")
    # ax.set_ylim(-60, 20)
    ax.legend(['n ='+str(cv_count)], handlelength=0, handletextpad=0, frameon=False)
    plt.tight_layout()
    ax.xaxis.labelpad = 5
    ax.yaxis.labelpad = 5
    ax.minorticks_on()
    ax.tick_params(axis = 'both', direction='in', which='major', length=18, width=3)
    ax.tick_params(axis = 'both', direction='in', which='minor', length=9, width=3)
    ax.set_box_aspect(1)


    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3) 


    # plt.savefig(os.path.join(savefig_directory, savefig_name), dpi=500)
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=1, vmax=len(file_list)))
    cbar = plt.colorbar(sm, fraction=0.046, pad=0.04)
    cbar.set_label('CV Number', rotation=270, fontweight='bold', labelpad=40, fontsize=35)
    cbar.outline.set_linewidth(3)
    cbar.ax.tick_params(labelsize=35)
    plt.show()



if __name__ == "__main__":
    main()

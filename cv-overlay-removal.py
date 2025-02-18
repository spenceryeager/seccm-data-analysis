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
    make_plot()


def make_plot():
    
    
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


    ##############################
    # some parameters to change
    directory = r"E:\RDrive_Backup\Spencer Yeager\papers\paper3_pbttt_annealing_kinetics\data\SECCM\06Feb2025_Nanoribbon\scan2"
    savefig_directory = r"E:\RDrive_Backup\Spencer Yeager\papers\paper3_pbttt_annealing_kinetics\figures\PublicationFigures\SECCM"
    savefig_name = "nanoribbon_Fc_overlay.png"
    sweep_numbers = 2
    fc_calibration = 0
    fc_ev = -4.9
    reference = "Potential (V) vs Ag Wire"
    ev_axis = False
    save = True
    color = '#e31a1c'
    ##############################

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
    

    for file in file_list[10:20]:


        if file.endswith('.csv'):
            cv_count += 1
            data = pd.read_csv(os.path.join(directory, file), sep='\t') # loading in data
            second_sweep = int(len(data) / sweep_numbers) # getting length of data file to remove first sweep
            smoothed_current = current_cleanup(data[i])
            # ax.plot(np.negative(data[v][second_sweep:] - fc_calibration), data[i][second_sweep:], color=color, alpha=0.05)
            ax.plot(np.negative(data[v][second_sweep:] - fc_calibration), smoothed_current[second_sweep:], color=color, alpha=0.05)




    # Formatting plot
    ax.invert_xaxis()
    ax.minorticks_on()
    ax.set_xlabel(reference)
    ax.set_ylabel("Current (pA)")
    ax.set_ylim(-60, 20)
    ax.legend(['n ='+str(cv_count)], handlelength=0, handletextpad=0, frameon=False)

    # ax2 = ax.secondary_xaxis("top", functions=(lambda x: (x-fc_ev)*-1, lambda x: (x+fc_ev)*-1))
    # ax2.minorticks_on()
    # ax2.set_xlabel("Energy vs. Vacuum (eV)")
    plt.tight_layout()
    ax.xaxis.labelpad = 5
    ax.yaxis.labelpad = 5
    ax.minorticks_on()
    ax.tick_params(axis = 'both', direction='in', which='major', length=18, width=3)
    ax.tick_params(axis = 'both', direction='in', which='minor', length=9, width=3)
    ax.set_box_aspect(1)


    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3) 

    plt.savefig(os.path.join(savefig_directory, savefig_name), dpi=500)
    plt.show()



if __name__ == "__main__":
    main()

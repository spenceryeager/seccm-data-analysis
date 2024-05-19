# Overlay of all CVs collected with 'n =' displayed as a legend.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import matplotlib as mpl
from matplotlib import rcParams
<<<<<<< HEAD
from matplotlib.lines import Line2D
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
=======
>>>>>>> 575c8174aa9702774ccd1e2c0fc9671e07ffadb0
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'
<<<<<<< HEAD
rcParams['savefig.dpi'] = 300
=======

>>>>>>> 575c8174aa9702774ccd1e2c0fc9671e07ffadb0


def main():
    make_plot()


def make_plot():
    
    
    def current_cleanup(current_data):
        sav_gol = signal.savgol_filter(current_data, 10, 3)
        gauss_current = ndimage.gaussian_filter1d(sav_gol, 20)
        cleaned_current = np.negative(gauss_current)
    return cleaned_current

    
    ##############################
    # some parameters to change
    directory = r"dir"
    savefig_directory = r"dir"
    savefig_name = "name"
    sweep_numbers = 3
    fc_calibration = 0.425
    fc_ev = -4.9
    reference = "Potential (V) vs Fc/Fc$^{+}$"
    ev_axis = False
    save = True
    ##############################

    # Setting font size before making plot
    fontsize = 40
    mpl.rcParams.update({'font.size': fontsize, 'figure.autolayout': True})

<<<<<<< HEAD
    directory = r"C:\Data\Spencer\2024\07May2024_PBTTT_Annealing_Study\ascast_withFc\scan"
=======
>>>>>>> 575c8174aa9702774ccd1e2c0fc9671e07ffadb0
    file_list = os.listdir(directory)
    v = 'Voltage (V)'
    i = 'Current (pA)'
    
<<<<<<< HEAD
    # some parameters to change
    sweep_numbers = 3
    fc_calibration = 0
    fc_ev = 0

    # creating plot
    fontsize = 40
    mpl.rcParams.update({'font.size': fontsize, 'figure.autolayout': True})
=======


    # creating plot
>>>>>>> 575c8174aa9702774ccd1e2c0fc9671e07ffadb0
    fig, ax = plt.subplots(figsize=(14,10), tight_layout=True)
    cv_count = 0


    for file in file_list:


        if file.endswith('.csv'):
            cv_count += 1
            data = pd.read_csv(os.path.join(directory, file), sep='\t') # loading in data
            second_sweep = int(len(data) / sweep_numbers) # getting length of data file to remove first sweep
<<<<<<< HEAD
            ax.plot(np.negative(data[v][second_sweep:] - fc_calibration), data[i][second_sweep:], color='#ff0000', alpha=0.05)
=======
            ax.plot((data[v][second_sweep:] - fc_calibration) * -1, data[i][second_sweep:], color='red', alpha=0.2)


>>>>>>> 575c8174aa9702774ccd1e2c0fc9671e07ffadb0

    # Formatting plot
    ax.invert_xaxis()
    ax.minorticks_on()
<<<<<<< HEAD
    ax.set_xlabel("Potential (V) vs. Ag/AgCl")
    ax.set_ylabel("Current (pA)")
    ax.set_ylim(-25, 5)
    ax.legend(['n ='+str(cv_count)], handlelength=0, handletextpad=0, frameon=False)

    # ax2 = ax.secondary_xaxis("top", functions=(lambda x: (x-fc_ev)*-1, lambda x: (x+fc_ev)*-1))
    # ax2.minorticks_on()
    # ax2.set_xlabel("Energy vs. Vacuum (eV)")
    plt.tight_layout()
    ax.xaxis.labelpad = 5
    ax.yaxis.labelpad = 5
    ax.tick_params(axis = 'both', direction='in', which='both', length=18, width=3)


    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3) 

    plt.savefig(r'C:\Users\spenceryeager\Pictures\dissertation_figs\ascast_fc_overlay')
    # plt.show()
=======
    ax.set_xlabel(reference)
    ax.set_ylabel("Current (pA)")
    ax.legend(['n ='+str(cv_count)], handlelength=0, handletextpad=0, frameon=False)

    ax.xaxis.labelpad = 5
    ax.yaxis.labelpad = 5
    ax.tick_params(axis = 'both', direction='in', which='both', length=18, width=3)
    

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3)


    if ev_axis:
        ax2 = ax.secondary_xaxis("top", functions=(lambda x: (x-fc_ev)*-1, lambda x: (x+fc_ev)*-1))
        ax2.minorticks_on()
        ax2.set_xlabel("Energy vs. Vacuum (eV)")
        ax2.tick_params(axis = 'both', direction='in', which='both', length=18, width=3)


        for axis in ['top','bottom','left','right']:
            ax2.spines[axis].set_linewidth(3)


    if save:
        plt.savefig(os.path.join(savefig_directory, savefig_name), dpi='figure')
    
    plt.show()
>>>>>>> 575c8174aa9702774ccd1e2c0fc9671e07ffadb0



if __name__ == "__main__":
    main()

# Overlay of all CVs collected with 'n =' displayed as a legend.

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import os
import numpy as np
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'


def main():
    make_plot()


def make_plot():
    ###########################
    # some parameters to change
    directory = r"\\engr-drive.bluecat.arizona.edu\Research\Ratcliff\Spencer Yeager\data\NiOx_Project\2023\09_Sep\25Sep2023_PtButtonCellIodide\Fc_Mini-Scan"
    sweep_numbers = 3
    fc_calibration = 0.0
    fc_ev = -4.9
    reference = "Potential (V) vs Ag Wire"
    ev_axis = False
    ###########################

    # Setting font size before making plot
    fontsize = 40
    mpl.rcParams.update({'font.size': fontsize, 'figure.autolayout': True})

    file_list = os.listdir(directory)
    v = 'Voltage (V)'
    i = 'Current (pA)'
    



    # creating plot
    fig, ax = plt.subplots(figsize=(14,10), tight_layout=True)
    cv_count = 0
    current_list = []


    for file in file_list:


        if file.endswith('.csv'):
            cv_count += 1
            data = pd.read_csv(os.path.join(directory, file), sep='\t') # loading in data
            second_sweep = int(len(data) / sweep_numbers) # getting length of data file to remove first sweep
            second_sweep = second_sweep * 2


            if cv_count == 1:
                current_list.append(data[i][second_sweep:].to_numpy())
                potentials = data[v][second_sweep:].to_numpy()
            else:
                current_list.append((data[i][second_sweep:].to_numpy()))


    avg_current = np.average(current_list, axis=0)
    avg_current_len = len(avg_current)
    std_current = np.std(current_list, axis=0)
    upper_bound = avg_current + std_current
    lower_bound = avg_current - std_current


    # sweep 1 plot
    ax.plot(np.negative(potentials[:int(avg_current_len/2)]), avg_current[:int(avg_current_len/2)], color='red', linewidth=7)
    ax.fill_between(np.negative(potentials[:int(avg_current_len/2)]), y1 = (avg_current[:int(avg_current_len/2)] + std_current[:int(avg_current_len/2)]), y2 = (avg_current[:int(avg_current_len/2)] - std_current[:int(avg_current_len/2)]), color='red', linewidth=0, alpha=0.4, interpolate=True)

    # sweep 2 plot
    ax.plot(np.negative(potentials[int(avg_current_len/2):]), avg_current[int(avg_current_len/2):], color='red', linewidth=7)
    ax.fill_between(np.negative(potentials[int(avg_current_len/2):]), y1 = (avg_current[int(avg_current_len/2):] + std_current[int(avg_current_len/2):]), y2 = (avg_current[int(avg_current_len/2):] - std_current[int(avg_current_len/2):]), color='red', linewidth=0, alpha=0.4, interpolate=True)

    # ax.plot(np.negative(potentials), (avg_current - std_current), color='black')

    # Formatting plot
    ax.invert_xaxis()
    ax.minorticks_on()
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


    # plt.savefig(r"\\engr-drive.bluecat.arizona.edu\Research\Ratcliff\Papers in Progress 2023\Perovskites\Iodide-Redox-On-NiOx\Figures\ferrocene_calib.svg")
    plt.show()



if __name__ == "__main__":
    main()
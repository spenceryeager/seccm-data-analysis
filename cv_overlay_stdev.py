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
    # Setting font size before making plot
    fontsize = 40
    mpl.rcParams.update({'font.size': fontsize, 'figure.autolayout': True})

    directory = r"R:\Spencer Yeager\data\NiOx_Project\2023\09_Sep\25Sep2023_PtButtonCellIodide\Fc_Mini-Scan"
    file_list = os.listdir(directory)
    v = 'Voltage (V)'
    i = 'Current (pA)'
    
    # some parameters to change
    sweep_numbers = 3
    fc_calibration = 0.0
    fc_ev = -4.9
    reference = "Potential (V) vs Ag Wire"
    ev_axis = False


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
            # ax.plot(data[v][second_sweep:] * -1, data[i][second_sweep:], color='dodgerblue', alpha=0.05, linewidth=7)
    avg_current = np.average(current_list, axis=0)
    avg_current_len = len(avg_current)
    std_current = np.std(current_list, axis=0)
    print(std_current)
    upper_bound = avg_current + std_current
    lower_bound = avg_current - std_current
    print(avg_current)
    print(upper_bound)
    # print(potentials)
    ax.plot(np.negative(potentials[:int(avg_current_len/2)]), avg_current[:int(avg_current_len/2)], color='red', linewidth=7)
    # ax.fill_between(np.negative(potentials), y1 = (avg_current + std_current), y2 = (avg_current - std_current), color='red', linewidth=7, alpha=0.4, interpolate=True)


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


    # if ev_axis:
    #     ax2 = ax.secondary_xaxis("top", functions=(lambda x: (x-fc_ev)*-1, lambda x: (x+fc_ev)*-1))
    #     ax2.minorticks_on()
    #     ax2.set_xlabel("Energy vs. Vacuum (eV)")


    # # plt.savefig(r'dir')
    plt.show()



if __name__ == "__main__":
    main()
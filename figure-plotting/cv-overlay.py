# Overlay of all CVs collected with 'n =' displayed as a legend.

import matplotlib.pyplot as plt
import pandas as pd
import os


def main():
    make_plot()


def make_plot():
    # Setting font size before making plot
    font = {'size': 12}
    plt.rc('font', **font)

    directory = r'dir'
    file_list = os.listdir(directory)
    v = 'Voltage (V)'
    i = 'Current (pA)'
    
    # some parameters to change
    sweep_numbers = 3
    fc_calibration = 0.5
    fc_ev = -4.9

    # creating plot
    fig, ax = plt.subplots(dpi=300)
    cv_count = 0
    for file in file_list:
        if file.endswith('.csv'):
            cv_count += 1
            data = pd.read_csv(os.path.join(directory, file), sep='\t') # loading in data
            second_sweep = int(len(data) / sweep_numbers) # getting length of data file to remove first sweep
            ax.plot(data[v][second_sweep:] - fc_calibration, data[i][second_sweep:] * -1, color='red', alpha=0.05)

    # Formatting plot
    ax.invert_xaxis()
    ax.minorticks_on()
    ax.set_xlabel("Potential vs. Fc/Fc$^{+}$")
    ax.set_ylabel("Current pA)")
    ax.legend(['n ='+str(cv_count)], handlelength=0, handletextpad=0)

    ax2 = ax.secondary_xaxis("top", functions=(lambda x: (x-fc_ev)*-1, lambda x: (x+fc_ev)*-1))
    ax2.minorticks_on()
    ax2.set_xlabel("Energy vs. Vacuum (eV)")
    plt.tight_layout()   
    # plt.savefig(r'dir')
    plt.show()



if __name__ == "__main__":
    main()
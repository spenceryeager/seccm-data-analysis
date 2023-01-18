# Overlay of all CVs collected with 'n =' displayed as a legend.

import matplotlib.pyplot as plt
import pandas as pd
import os


def main():
    make_plot()


def make_plot():
    directory = r'dir'
    file_list = os.listdir(directory)
    v = 'Voltage (V)'
    i = 'Current (pA)'
    
    # some parameters to change
    sweep_numbers = 3
    fc_calibration = 0.5

    # creating plot
    fig, ax = plt.subplots()
    cv_count = 0
    for file in file_list:
        if file.endswith('.csv'):
            cv_count += 1
            data = pd.read_csv(os.path.join(directory, file), sep='\t') # loading in data
            second_sweep = int(len(data) / sweep_numbers) # getting length of data file to remove first sweep
            
            ax.plot(data[v][second_sweep:] - fc_calibration, data[i][second_sweep:] * -1, color='red', alpha=0.1)

    # Formatting plot
    ax.invert_xaxis()
    ax.minorticks_on()
    ax.set_xlabel("Potential vs. Fc/Fc$^{+}$")
    ax.set_ylabel("Current pA)")
    ax.legend(['n ='+str(cv_count)], handlelength=0, handletextpad=0)    
    plt.show()



if __name__ == "__main__":
    main()
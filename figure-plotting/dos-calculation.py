# Obtaining density of states from SECCM data

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp


def main():
    dos_calculation()


def dos_calculation():
    # fill this section out beforehand
    fc_correction = 0 # how much do we need to adjust the potential based on Fc redox potential?
    sweeps = 3 # how many sweeps are there? this helps with determining sweep cutoffs
    

    filepath = r"filepath"
    datafile = pd.read_csv(filepath, sep='\t')
    sweep_segments = int(len(datafile)/sweeps)
    print(sweep_segments)


    fig, ax = plt.subplots()
    ax.plot(datafile['Voltage (V)'][sweep_segments:sweep_segments*2], datafile['Current (pA)'][sweep_segments:sweep_segments*2] * -1, color='red')
    ax.invert_xaxis()
    plt.show()


if __name__ == "__main__":
    main()
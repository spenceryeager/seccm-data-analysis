# this will be used to iterate over all recorded CVs and extract kinetics parameters, such as transfer coefficients and rate constants.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def main():
    data_path = r"D:\Research\SPECS-Project\2023\18Feb2023_rrP3HT_500nm-tip-Fc\scan\0X_2Y_rrP3HT-Fc.csv"
    data = pd.read_csv(data_path, sep='\t')
    length = len(data)
    ox_start = int(length/3)
    ox_end = ox_start + int(ox_start/2)
    
    fig, ax = plt.subplots()
    ax.plot(data['Voltage (V)'][ox_start:ox_end], data['Current (pA)'][ox_start:ox_end])
    plt.show()


if __name__ == "__main__":
    main()
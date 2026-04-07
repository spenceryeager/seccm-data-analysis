import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy as sp
from oldham_zoski_sim import sigmoid_maker

# This will ideally take the kinetics parameters from the experimental voltammograms, generate a sigmoid, and check the goodness of fit.

def main():
    calculated_values = r"G:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\worked-up-data\SECCM_Kinetics\Bard-Mirkin\P3HT\P3HT_final_kinetics_06April2026.csv"
    combined_voltammograms = r"G:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\worked-up-data\SECCM_Kinetics\Bard-Mirkin\P3HT\p3ht_combined_cleaned_voltammograms.csv"
    calculated_values = pd.read_csv(calculated_values)
    combined_voltammograms = pd.read_csv(combined_voltammograms)
    print(calculated_values.head())

    e = combined_voltammograms['Potential (V)']
    do = 4.1 * 10**-6
    eo = 0.367
    a = 2.7 * 10**-5
    kappa_naught = 0.217586
    alpha = 0.864492
    
    solved_voltammogram = sigmoid_maker(do=do, dr=do, n=1, a=a,e=e, eo=eo, ko=kappa_naught, transfer_coef=alpha)
    fig, ax = plt.subplots()
    ax.plot(e, solved_voltammogram)
    ax.plot(combined_voltammograms['Potential (V)'], combined_voltammograms['0X_0Y_p3ht-with-fc.csv Normalized Current (pA)'])

    ax.invert_xaxis()
    plt.show()

if __name__ == "__main__":
    main()
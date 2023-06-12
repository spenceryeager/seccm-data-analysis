# this takes the output file from batch_kinetics_processing.py and does statistical analysis on it

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    kinetics_file = r"C:\Users\spenceryeager\Documents\seccm-data\analysis_folder\results.csv"
    kinetics_data = pd.read_csv(kinetics_file)
    observations = kinetics_data['log10 Rate Constant'].count()
    bin_num = sturges_rule(observations)
    plotting(kinetics_data, bin_num)


def sturges_rule(observations):
    bin_num = int(np.ceil(np.log2(observations) + 1))
    return bin_num


def plotting(data, bin_num):
    fig, ax = plt.subplots()
    ax.hist(data['log10 Rate Constant'], bin_num, edgecolor='royalblue', color='dodgerblue')
    plt.show()


if __name__ == "__main__":
    main()

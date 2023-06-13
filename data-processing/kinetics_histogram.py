# this takes the output file from batch_kinetics_processing.py and does statistical analysis on it

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    kinetics_file = r"D:\Research\SPECS-Project\2023\24Mar2023_P3HT-with-Fc\analysis_folder\results_with_bounds.csv"
    kinetics_file_2 = r"D:\Research\SPECS-Project\2023\28Mar2023_PBTTT_Fc\analysis\results_with_bounds.csv"
    kinetics_data = pd.read_csv(kinetics_file)
    kinetics_data_2 = pd.read_csv(kinetics_file_2)
    observations = kinetics_data['log10 Rate Constant'].count()
    bin_num = sturges_rule(observations)
    plotting(kinetics_data, kinetics_data_2, bin_num)


def sturges_rule(observations):
    bin_num = int(np.ceil(np.log2(observations) + 1))
    return bin_num


def plotting(data, data2, bin_num):
    fig, ax = plt.subplots()
    ax.hist(data['log10 Rate Constant'], bin_num, edgecolor='royalblue', color='dodgerblue')
    ax.hist(data2['log10 Rate Constant'], bin_num, edgecolor='firebrick', color='red')
    plt.show()


if __name__ == "__main__":
    main()

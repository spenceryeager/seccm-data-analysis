# this takes the output file from batch_kinetics_processing.py and does statistical analysis on it

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


def main():
    kinetics_file = r"C:\Users\spenceryeager\Documents\seccm-data\24Mar2023_P3HT-with-Fc\analysis\results_with_bounds.csv"
    kinetics_file_2 = r"C:\Users\spenceryeager\Documents\seccm-data\28Mar2023_PBTTT_Fc\analysis\results_with_bounds.csv"
    kinetics_data = pd.read_csv(kinetics_file)
    kinetics_data_2 = pd.read_csv(kinetics_file_2)
    
    mu1, sigma1, fwhm1 = gauss_fitting(kinetics_data['log10 Rate Constant'])
    x_vals = np.linspace(-4, -1, 1000)
    kd1_gauss = norm.pdf(x_vals, mu1, sigma1) * 70

    mu2, sigma2, fwhm2 = gauss_fitting(kinetics_data_2['log10 Rate Constant'])
    kd2_gauss = norm.pdf(x_vals, mu2, sigma2) * 30

    observations = kinetics_data['log10 Rate Constant'].count()
    bin_num = sturges_rule(observations)
    plotting(kinetics_data, kinetics_data_2, x_vals, kd1_gauss, kd2_gauss, bin_num)


def sturges_rule(observations):
    bin_num = int(np.ceil(np.log2(observations) + 1))
    return bin_num


def gauss_fitting(spread):
    mu, sigma = norm.fit(spread)
    fwhm = 2.355 * sigma
    return mu, sigma, fwhm


def plotting(data, data2, gauss1x, gauss1y, gauss2y, bin_num):
    font = {'size': 14}
    plt.rc('font', **font)
    fig, ax = plt.subplots(2)
    ax[0].hist(data['log10 Rate Constant'], edgecolor='royalblue', color='dodgerblue', label='rr-P3HT')
    ax[0].plot(gauss1x, gauss1y, color='darkslategray')
    ax[1].hist(data2['log10 Rate Constant'], bin_num, edgecolor='firebrick', color='red', label='PBTTT')
    ax[1].plot(gauss1x, gauss2y, color='darkred')
    ax[1].set_xlabel('log$_{10}$ $k_{0}$')
    ax[1].set_ylabel('Counts')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()

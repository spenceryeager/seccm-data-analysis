import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as constant
import pandas as pd
from oldham_zoski_sim import sigmoid_maker

def main():
    # Test
    do = 4.1 * (10 ** -6) # cm2 / s, diffusion coefficient
    dr = do # we assume the diffusion of the redox probe is the same in the oxidized and reduced state
    n = 1 # number of electrons transfered
    a = 2.7 * (10 **-5) # radius of tip, in cm # This is NOT USED! 
    eo = 0 # formal potential
    e = np.linspace(-1, 1, 10000) # potential range
    # e = e - eo
    # kappanaught = 5
    # transfer_coef = 0.5 # transfer coefficient
    kappanaught_list = np.linspace(2,20,2)
    alpha_list = np.linspace(0,1,5)
    reduction = True # are we looking at a reduction process or an oxidation process?
    # for 
    for kappanaught in kappanaught_list:

        for transfer_coef in alpha_list:

            val = sigmoid_maker(do, dr, n, a, e, eo, kappanaught, transfer_coef, reduction)
            voltammogram = pd.DataFrame(columns=['Potential (V)', 'Normalized Current'])
            voltammogram['Potential (V)'] = e
            voltammogram['Normalized Current'] = val


            if reduction:
                one_quart = voltammogram.loc[(voltammogram['Normalized Current'] - 0.25).abs().argsort()[0]]
                one_half = voltammogram.loc[(voltammogram['Normalized Current'] - 0.5).abs().argsort()[0]]
                three_quart = voltammogram.loc[(voltammogram['Normalized Current'] - 0.75).abs().argsort()[0]]


            else:
                # one_quart = voltammogram.loc[np.round(voltammogram['Normalized Current'], 2) == -0.25].median()
                one_quart = voltammogram.loc[(voltammogram['Normalized Current'] - -0.25).abs().argsort()[0]]
                one_half = voltammogram.loc[(voltammogram['Normalized Current'] - -0.5).abs().argsort()[0]]
                three_quart = voltammogram.loc[(voltammogram['Normalized Current'] - -0.75).abs().argsort()[0]]

            print((one_half['Potential (V)'] * 1000))
            visualize(voltammogram, one_quart, one_half, three_quart, reduction)


def visualize(voltammogram, one_quart, one_half, three_quart, reduction):
    fig, ax = plt.subplots()
    ax.plot(voltammogram['Potential (V)'], voltammogram['Normalized Current'])
    ax.set_xlim(-0.6, 0.6)
    ax.invert_xaxis()
    ax.set_xlabel("Potential (V)")
    ax.set_ylabel('Normalized Current')
    if reduction:
        ax.vlines(x = one_quart['Potential (V)'], ymin=0, ymax=1, color='red', alpha=0.25, label = "1/4 Current")
        ax.vlines(x = one_half['Potential (V)'], ymin=0, ymax=1, color='black', alpha=0.25, label = '1/2 Current')
        ax.vlines(x = three_quart['Potential (V)'], ymin=0, ymax=1, color='blue', alpha=0.25, label= '3/4 Current')

    else:
        ax.vlines(x = one_quart['Potential (V)'], ymin=-1, ymax=0, color='red', alpha=0.25, label = "1/4 Current")
        ax.vlines(x = one_half['Potential (V)'], ymin=-1, ymax=0, color='black', alpha=0.25, label = '1/2 Current')
        ax.vlines(x = three_quart['Potential (V)'], ymin=-1, ymax=0, color='blue', alpha=0.25, label= '3/4 Current')    
    
    
    ax.legend()
    plt.show()

if __name__ == '__main__':
    main()
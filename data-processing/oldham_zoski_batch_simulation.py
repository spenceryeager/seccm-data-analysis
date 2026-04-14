import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as constant
import pandas as pd
import os
from oldham_zoski_sim import sigmoid_maker

def main():
    file_path = r'data-processing\sigmoid_simulation_values'
    file_name = 'reduction'
    do = 4.1 * (10 ** -6) # cm2 / s, diffusion coefficient
    dr = do # we assume the diffusion of the redox probe is the same in the oxidized and reduced state
    n = 1 # number of electrons transfered
    a = 2.7 * (10 **-5) # radius of tip, in cm # This is NOT USED! 
    eo = 0.5 # formal potential
    e = np.linspace(-2, 2, 10000) # potential range
    # e = e - eo
    # kappanaught_list = [5]
    # alpha_list = [0.5] # transfer coefficient
    kappanaught_list = np.linspace(0.2,20,1001)
    alpha_list = np.linspace(0,1,101)
    reduction = True # are we looking at a reduction process or an oxidation process?
    visualize_and_print = False
    # visualize_and_print = True

    value_df = pd.DataFrame(columns=['dE1/4 - dE3/4 (mV)', "dEo - dE1/2 (mV)", "Transfer Coefficient", "KappaNaught"])
    delta_quartile = []
    delta_half =[]
    alpha = []
    kn_list = []




    for transfer_coef in alpha_list:

        for kappanaught in kappanaught_list:

            val = sigmoid_maker(do, dr, n, a, e, eo, kappanaught, transfer_coef, reduction)
            voltammogram = pd.DataFrame(columns=['Potential (V)', 'Normalized Current'])
            voltammogram['Potential (V)'] = e
            voltammogram['Normalized Current'] = val


            if reduction:
                one_quart = voltammogram.loc[(voltammogram['Normalized Current'] - 0.25).abs().argsort()].mean()
                one_half = voltammogram.loc[(voltammogram['Normalized Current'] - 0.5).abs().argsort()].mean()
                three_quart = voltammogram.loc[(voltammogram['Normalized Current'] - 0.75).abs().argsort()].mean()


            else:
                one_quart = voltammogram.loc[(voltammogram['Normalized Current'] - -0.25).abs().argsort()].mean()
                one_half = voltammogram.loc[(voltammogram['Normalized Current'] - -0.5).abs().argsort()].mean()
                three_quart = voltammogram.loc[(voltammogram['Normalized Current'] - -0.75).abs().argsort()].mean()

            
            # List Appending
            comparison_one = (np.abs(one_quart['Potential (V)'] - three_quart['Potential (V)']) * 1000) < 300
            comparison_two = (np.abs(eo - one_half['Potential (V)']) * 1000) < 500

            if comparison_one and comparison_two:
                delta_quartile.append(np.abs(one_quart['Potential (V)'] - three_quart['Potential (V)']) * 1000)
                delta_half.append((np.abs(eo - one_half['Potential (V)']) * 1000))
                alpha.append(transfer_coef)
                kn_list.append(kappanaught)
            
            else:
                delta_quartile.append(np.nan)
                delta_half.append(np.nan)
                alpha.append(transfer_coef)
                kn_list.append(kappanaught)

                
            # Visualization and Printing Values
            if visualize_and_print:
                print("########")
                print("E1/2 (mV)", np.abs(np.abs(eo - one_half['Potential (V)']) * 1000))
                print("E1/4 - E3/4 (mV)",np.abs(one_quart['Potential (V)'] - three_quart['Potential (V)']) * 1000)
                print("Transfer Coefficient:", transfer_coef)
                print("KappaNaught:", kappanaught)
                visualize(voltammogram, one_quart, one_half, three_quart, reduction)


    # Dataframe Saving
    value_df['dE1/4 - dE3/4 (mV)'] = delta_quartile
    value_df['dEo - dE1/2 (mV)'] = delta_half
    value_df['Transfer Coefficient'] = alpha
    value_df['KappaNaught'] = kn_list

    print(value_df.head())
    value_df.to_csv(os.path.join(file_path, (file_name + "_quartile_values_with_nan.csv")), index=False)
    value_df.dropna().to_csv(os.path.join(file_path, (file_name + "_quartile_values_no_nan.csv")), index=False)

def visualize(voltammogram, one_quart, one_half, three_quart, reduction):
    fig, ax = plt.subplots()
    ax.plot(voltammogram['Potential (V)'], voltammogram['Normalized Current'])
    ax.set_xlim(-0.2, 1)
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
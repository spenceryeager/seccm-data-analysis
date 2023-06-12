# this takes a folder of SECCM kinetics data and gets kinetics info from it
# big note here: currently, this program uses UME metal electrode approximations.
# take the results here with a grain of salt, butler-volmer kinetics are not formulated for semiconductors/polymers.

import pandas as pd
import numpy as np
from bard_mirkin_kinetics import get_kinetics
import os


def main():
    directory = r"C:\Users\spenceryeager\Documents\seccm-data\18Feb2023_rrP3HT_500nm-tip-Fc\scan"
    save_dir = r"C:\Users\spenceryeager\Documents\seccm-data\analysis_folder"
    save_name = 'results.csv'
    filelist = os.listdir(directory)
    # print(filelist)
    linear_region = [0.15, 0.29] # Defining start and end of linear region for background correction
    formal_potential = 0.4 # V, formal redox potential of probe
    id_potential = 0.2 # V, potential where diffusion-limited current is observed
    diffusion_coef = 1 * (10 ** -6) # cm2/s
    tip_radius = 2.5 * (10 **-5) #cm
    potential_range = [0.7, 0.10] # V!
    sweep_number = 3
    kinetics_df = pd.DataFrame(columns = ['Rate Constant (cm/s)', 'log10 Rate Constant', "Transfer Coefficient", "Transfer Coefficient Error", "KappaNaught", "KappaNaught Error"])
    rate_constant_list = []
    transfer_coef_list = []
    transfer_coef_error_list = []
    kappa_naught_list = []
    kappa_naught_error_list = []

    for filename in filelist:

        if os.path.isfile(os.path.join(directory,filename)):

            data_path = os.path.join(directory,filename)
            rate_constant, kappa_naught, kappa_naught_error, transfer_coef, transfer_coef_error = get_kinetics(data_path, linear_region, potential_range=potential_range, sweep=sweep_number, diffusion_current_potential=id_potential, diffusion_coefficient=diffusion_coef, tip_radius=tip_radius, plotting=False)
            rate_constant_list.append(rate_constant)
            transfer_coef_list.append(transfer_coef)
            transfer_coef_error_list.append(transfer_coef_error)
            kappa_naught_list.append(kappa_naught)
            kappa_naught_error_list.append(kappa_naught_error)
        else:
            print('skip')



    kinetics_df['Rate Constant (cm/s)'] = rate_constant_list
    kinetics_df['log10 Rate Constant'] = np.log10(rate_constant_list)
    kinetics_df['Transfer Coefficient'] = transfer_coef_list
    kinetics_df['Transfer Coefficient Error'] = transfer_coef_error_list
    kinetics_df['KappaNaught'] = kappa_naught_list
    kinetics_df['KappaNaught Error'] = kappa_naught_error_list
    
    kinetics_df.to_csv(os.path.join(save_dir, save_name))


if __name__ == "__main__":
    main()
    
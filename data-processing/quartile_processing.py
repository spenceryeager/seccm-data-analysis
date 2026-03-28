import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy as sp


def main():
    # test values
    dehalf = 0.03
    dquart = 0.07
    test_df = pd.DataFrame(columns=['alpha', 'kn'])

    ## Constants for rate determination
    do = 4.1 * (10 ** -6) # cm2 / s
    radius = 2.7 * (10 **-5) #cm

    data_analysis_file = r"E:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\worked-up-data\SECCM_Kinetics\Bard-Mirkin\P3HT\p3ht_results_final.csv"
    data_analysis_file = pd.read_csv(data_analysis_file)
    data_save_directory = r"E:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\worked-up-data\SECCM_Kinetics\Bard-Mirkin\P3HT"
    data_save_name = r"P3HT_final_kinetics"

    quartile_file = r'data-processing\quartile_kappa_alpha_values\quartile_values_unabridged_cleaned.csv' # relative to where this is being run
    quartile_processing_loading = pd.read_csv(quartile_file)

    alpha_list = []
    kn_list = []


    for index, row in data_analysis_file.iterrows():
        dehalf = row['dE1/2_E0'].round(3).item()
        dquart = row['dE1/4_3/4'].round(3).item()
        # print(dquart, dehalf)
        alpha, kn = data_filtering(quartile_processing_loading, dehalf, dquart)
        alpha_list.append(alpha)
        kn_list.append(kn)

    rate_array = np.asarray(kn_list)
    rate_val = ((4 * do) * rate_array) / (np.pi * radius)
    data_analysis_file['alpha'] = alpha_list
    data_analysis_file['kappa_naught'] = kn_list
    data_analysis_file['Rate Coefficient (cm/s)'] = rate_val

    data_analysis_file.to_csv(os.path.join(data_save_directory, (data_save_name + ".csv")), index=False)

    # test dataframe
    # test_df['alpha'] = alpha_list
    # test_df['kn'] = kn_list
    # test_df.to_csv(r"path")

    # single value detemination, mostly for debugging
    # alpha, kn = data_filtering(quartile_processing_loading, dehalf, dquart)
    # print(alpha, "alpha")
    # print(kn, "kappa naught")


def data_filtering(quartile_processing_loading, dehalf, dquart):
    filtered_df = quartile_processing_loading.copy()
    filtered_df['E1/4 - E 3/4 (mV)'] = (filtered_df['E1/4 - E 3/4 (mV)'] - (dquart * 1000)).abs()

    filtered_df['dE 1/2 (mV)'] = (filtered_df['dE 1/2 (mV)'] - (dehalf * 1000)).abs()
    
    # Ideally, the subtracted value will be 0. This is never the case, it will be close to zero but not exactly zero. Due to the thousands of values in the table, filtering by values that are "close" to 0 means we can affectively get the actual value. Changing the value of 2 to 1 to 0.1 results in very minimal difference. for Example, the percent difference of  a value calulated between the filter value of 2 and 1 is about 0.42%, i.e. very minimal.

    filtered_df = filtered_df.loc[filtered_df['E1/4 - E 3/4 (mV)'] < 2 ]
    filtered_df = filtered_df.loc[filtered_df['dE 1/2 (mV)'] < 2 ]

    # print(quartile_processing_loading.head())
    # print((quartile_processing_loading.sort_values('dE 1/2 (mV)'))) 
    # print(quartile_processing_loading.sort_values('dE 1/2 (mV)', ascending=True))
    alpha = filtered_df['Alpha'].mean()
    kn = filtered_df['KappaNaught'].mean()

    return alpha, kn


if __name__ == "__main__":
    main()

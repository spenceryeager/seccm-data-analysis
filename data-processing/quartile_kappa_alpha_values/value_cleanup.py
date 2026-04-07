# this is just a small utility script to clean up the kinetics values

import pandas as pd
import os


def main():
    quartile_file = r"data-processing\quartile_kappa_alpha_values\quartile_vals_large_unabridged.csv" 
    # path is relative to where I'm running it
    save_file = r'data-processing\quartile_kappa_alpha_values'
    savename = 'quartile_values_large_unabridged_cleaned'
    quartile_values = pd.read_csv(quartile_file)
    quartile_values = quartile_values.dropna()

    quartile_values = quartile_values.loc[quartile_values['1/4 fsolve check (should be zero)'] < 1]
    quartile_values = quartile_values.loc[quartile_values['1/2 fsolve check'] < 1]
    quartile_values = quartile_values.loc[quartile_values['3/4 fsolve check'] < 1]
    quartile_values = quartile_values.sort_values(by='E1/4 - E 3/4 (mV)')
    
    quartile_values.to_csv(path_or_buf=os.path.join(save_file, (savename + '.csv')), index=False)


    



if __name__ == '__main__':
    main()
# this takes a folder of SECCM kinetics data and gets kinetics info from it
# big note here: currently, this program uses UME metal electrode approximations.
# take the results here with a grain of salt, butler-volmer kinetics are not formulated for semiconductors/polymers.

import pandas as pd
import numpy as np
from bard_mirkin_kinetics import get_kinetics
import os


def main():
    directory = r"C:\Users\spenceryeager\Documents\seccm-data\test_dir"
    filelist = os.listdir(directory)
    print(filelist)
    linear_region = [0.15, 0.29] # Defining start and end of linear region for background correction
    formal_potential = 0.4 # V, formal redox potential of probe
    id_potential = 0.2 # V, potential where diffusion-limited current is observed
    diffusion_coef = 1 * (10 ** -6) # cm2/s
    tip_radius = 2.5 * (10 **-5) #cm
    for filename in filelist:
        data_path = os.path.join(directory,filename)
        rate_constant, kappa_naught, kappa_naught_error, transfer_coef, transfer_coef_error = get_kinetics(data_path, linear_region, diffusion_current_potential=id_potential, diffusion_coefficient=diffusion_coef, tip_radius=tip_radius, plotting=False)
        print(np.log10(rate_constant))

if __name__ == "__main__":
    main()
    
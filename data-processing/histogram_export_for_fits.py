import pandas as pd
import numpy as np
import os

def main():

    hist_data = pd.read_csv(r"E:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\worked-up-data\SECCM_Kinetics\PBTTT\results_with_bounds_pbttt.csv")
    column = "log10 Rate Constant"
    savedir = r"E:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\worked-up-data\SECCM_Kinetics\PBTTT"
    savename = "pbttt_histogram_for_fit.csv"

    bincount = sturges(len(hist_data[column]))
    hist_data_array, bin_locations = np.histogram((hist_data[column]), bins=bincount)

    midpoints = []

    bin_length = len(bin_locations)
    index = 0
    while ((index + 1) < bin_length):
        mid_val = (bin_locations[index] + bin_locations[index+1]) / 2
        midpoints.append(mid_val)
        index += 1

    fit_data = {'Midpoints' : midpoints, 'Counts' : hist_data_array}
    hist_vals = pd.DataFrame(fit_data)


    hist_vals.to_csv(os.path.join(savedir,savename))


def sturges(count):
    bins = int(np.ceil(np.log2(count) + 1))
    return bins


if __name__ == "__main__":
    main()
import pandas as pd
import numpy as np

def main():

    hist_data = pd.read_csv(r"sample")
    column = "sample_column"
    savefile = "save dir"

    bincount = sturges(len(hist_data[column]))
    hist_data_array, bin_locations = np.histogram(np.negative(hist_data[column]), bins=bincount)

    midpoints = []

    bin_length = len(bin_locations)
    index = 0
    while ((index + 1) < bin_length):
        mid_val = (bin_locations[index] + bin_locations[index+1]) / 2
        midpoints.append(mid_val)
        index += 1

    fit_data = {'Midpoints' : midpoints, 'Counts' : hist_data_array}
    hist_vals = pd.DataFrame(fit_data)


    hist_vals.to_csv(savefile)


if "__name__" == __main__:
    main()
# this will be used to iterate over all recorded CVs and extract kinetics parameters, such as transfer coefficients and rate constants.
# this is adopted from https://doi.org/10.1021/ac00043a020, which is not applicable to semiconductors. But can be used as an approximation
# this biggest assumption baked into this approximation is the electron transfer follows Butler Volmer kinetics.
# big fat note: this was formulated in the paper for REDUCTION events. If using an oxidation event, you must take this into account.
# What I mean by this is, three-quarter current should be on the reductive side (more negative) of E1/2, and quarter current should be on the oxidative side (more positive) of E1/2.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy.signal as signal
import scipy.ndimage as ndimage
import scipy.constants as constant
import scipy.stats as stats
from scipy.optimize import fsolve
from scipy.optimize import curve_fit
from oldham_zoski_sim import sigmoid_maker_curvefit


def main():
    # Fill this section out! Future implementation will have a popup box perhaps.
    linear_region = [0.26, 0.25] # Defining start and end of linear region for background correction
    formal_potential = 0.31 # V, formal redox potential of probe
    id_potential = 0.26 # V, potential where diffusion-limited current is observed
    diffusion_coef = 4.1 * (10 ** -6) # cm2/s
    tip_radius = 2.7 * (10 **-5) #cm
    potential_range = [0.6, 0.25] # V!
    sweep_number = 1
    sweeps = 1
    ox_to_red_event = False # Are you trying to 
    goofy_format = False # This is for when the SECCM is configured to record currents in US convention, thus making the potentials backward. Hopefully will be fixed in a future update of the SECCM software.
    plotting = True
    # working parts of code
    data_path = r"G:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\data\28Mar2023_PBTTT_Fc\scan\0X_0Y_pbttt_fc.csv"

    data = pd.read_csv(data_path, sep='\t')
    len_data = len(data)
    cycle_subset = int(len_data / sweeps)
    data_ox_cycle = int(cycle_subset / 2)
    data_subset = data[data_ox_cycle : data_ox_cycle*2].reset_index()


    h, q, tq = get_kinetics(data_loadin=data_subset, formal_potential=formal_potential, linear_region=linear_region,  potential_range=potential_range, sweep=sweep_number, diffusion_current_potential=id_potential, diffusion_coefficient=diffusion_coef, tip_radius=tip_radius, goofy_format = goofy_format, plotting=True, redox_event=ox_to_red_event)
    # print('ehalf','rate_constant', 'kappa_naught', "kappa naught error","transfer coef", "transfer coef error")
    # print(ehalf, rate_constant, kappa_naught, kappa_naught_error, transfer_coef, transfer_coef_error)

    print((abs(q - h)))
    print((abs(h - tq)))


def get_kinetics(data_loadin, formal_potential, linear_region, potential_range, sweep, diffusion_current_potential, diffusion_coefficient, tip_radius, goofy_format, plotting, redox_event):
    # data = pd.read_csv(data_path, sep='\t')
    data = data_loadin.copy() # doing this to avoid errors

    # This is an important part to consider when updating data output from the SECCM.
    if goofy_format:
        data['Voltage (V)'] *= -1
    else:
        data['Current (pA)'] *= -1

    loc1 = data.loc[data['Voltage (V)'] == potential_range[0]].index   
    loc2 = data.loc[data['Voltage (V)'] == potential_range[1]].index

    if loc1[0] < loc2[0]:
        data = data[loc1[0]:loc2[0]]
    else:
        data = data[loc2[0]:loc1[0]]

    cleaned_current = current_cleanup(data['Current (pA)'])
    corrected_current = background_correction(data, cleaned_current, linear_region[0], linear_region[1])
    corrected_current = background_zero(corrected_current)
    data['Zeroed Current (pA)'] = corrected_current
    data = data.reset_index(drop=True)
    data = get_id(diffusion_current_potential, data)
    h, q, tq = current_quartiles(data, redox_event) # q, h, tq = quarter, half, threequarter potentials


    if plotting:
        make_plot(data, q, h, tq)
    else:
        print("Analysizing next CV")
    
    # Rounding the quartiles
    h = rounding(h)
    q = rounding(q)
    tq = rounding(tq)
    return h, q, tq


# def get_kinetics(data, formal_potential, linear_region, potential_range, sweep, diffusion_current_potential, diffusion_coefficient, tip_radius, goofy_format, plotting):
#     # data = pd.read_csv(data_path, sep='\t')

#     # This is an important part to consider when updating data output from the SECCM.
#     if goofy_format:
#         data['Voltage (V)'] *= -1
#     else:
#         data['Current (pA)'] *= -1

#     loc1 = data.loc[data['Voltage (V)'] == potential_range[0]].index   
#     loc2 = data.loc[data['Voltage (V)'] == potential_range[1]].index

#     if loc1[0] < loc2[0]:
#         data = data[loc1[0]:loc2[0]]
#     else:
#         data = data[loc2[0]:loc1[0]]

#     cleaned_current = current_cleanup(data['Current (pA)'])
#     corrected_current = background_correction(data, cleaned_current, linear_region[0], linear_region[1]) # deprecated way of correcting current. Skews the trend in my opinion.
#     corrected_current = background_zero(corrected_current)
#     data['Zeroed Current (pA)'] = corrected_current
#     data = data.reset_index(drop=True)
#     data = get_id(diffusion_current_potential, data)
#     h, q, tq = current_quartiles(data) # q, h, tq = quarter, half, threequarter potentials
#     # e = data['Voltage (V)']

#     try:
#         # parameters, covariance = curve_fit(sigmoid_maker_curvefit, (data['Voltage (V)'] - 0.4), data['Normalized Current (pA)'], bounds=([-np.inf, 0],[20,1])) # adding bounds
#         # parameters, covariance = curve_fit(sigmoid_maker_curvefit, (data['Voltage (V)'] - formal_potential), data['Normalized Current (pA)'])
#         # approximation_currents = sigmoid_maker_curvefit((data['Voltage (V)'] - formal_potential), parameters[0], parameters[1])
#         parameters, covariance = curve_fit(sigmoid_maker_curvefit, (data['Voltage (V)'] - formal_potential), data['Normalized Current (pA)'])
#         approximation_currents = sigmoid_maker_curvefit((data['Voltage (V)']- formal_potential), parameters[0], parameters[1])
#         kappa_naught = parameters[0]
#         transfer_coef = parameters[1]
#         error_in_fits = np.sqrt(np.diag(covariance))
#         kappa_naught_error = error_in_fits[0]
#         transfer_coef_error = error_in_fits[1]
#         rate_constant = get_rate_constant(diffusion_coefficient, tip_radius, kappa_naught)
#         fit_success = True

#         ## This section is for saving a particular data set to a CSV file to show the fitting procedure in a          conference or something
        
#         # save_df = data
#         # save_df['Fit Current'] = approximation_currents
#         # save_directory = r"dir"
#         # save_name = r"name"
#         # save_df.to_csv(os.path.join(save_directory,(save_name + ".csv")))


#     except RuntimeError:
#         "Fit failed."
#         kappa_naught = np.nan
#         transfer_coef = np.nan
#         error_in_fits = np.nan
#         kappa_naught_error = np.nan
#         transfer_coef_error = np.nan
#         rate_constant = np.nan
#         approximation_currents = 0
#         fit_success = False

    
#     if plotting:
#         make_plot(data, approximation_currents, q, h, tq, fit_success)
#     else:
#         print("Analysizing next CV")

#     return rate_constant, kappa_naught, kappa_naught_error, transfer_coef, transfer_coef_error, h

    
def make_plot(data, q, h, tq):
    plt.rcParams['font.size'] = 14
    fig, ax = plt.subplots()
    # ax.plot(data['Voltage (V)'], data['Current (pA)'], color='purple', label='Raw')
    # ax.plot(data['Voltage (V)'], cleaned_current, color='red', label='Uncorrected')
    # ax.plot(data['Voltage (V)'], corrected_current, color='blue', label='Background corrected')

    ax.plot(data['Voltage (V)'], data['Normalized Current (pA)'], color='purple', label='Normalized')

    ax.set_xlabel("Potential (V) vs. Reference")
    ax.set_ylabel("Normalized Current")
    ax.vlines(x = q, ymin=0, ymax=1, color='red', alpha=0.25, label = "1/4 Current")
    ax.vlines(x = h, ymin=0, ymax=1, color='black', alpha=0.25, label = '1/2 Current')
    ax.vlines(x = tq, ymin=0, ymax=1, color='blue', alpha=0.25, label= '3/4 Current')

    ax.legend(loc = "best", fontsize = 12)
    ax.invert_xaxis()
    plt.show()


def get_rate_constant(diff_coef, radius, kappa_naught):
    rate_constant = (4 * diff_coef * kappa_naught) / (constant.pi * radius)
    return rate_constant


def current_cleanup(current_data):
    sav_gol = signal.savgol_filter(current_data, 10, 3)
    cleaned_current = ndimage.gaussian_filter1d(sav_gol, 15)
    return cleaned_current


def background_correction(data_subset, cleaned_current, lin_start, lin_end):
    data_subset = data_subset.reset_index(drop=True)
    lin_loc_1 = data_subset.loc[data_subset['Voltage (V)'] == lin_start].index[0]
    lin_loc_2 = data_subset.loc[data_subset['Voltage (V)'] == lin_end].index[0]

    if lin_loc_1 < lin_loc_2:
        index1 = lin_loc_1
        index2 = lin_loc_2
    else:
        index1 = lin_loc_2
        index2 = lin_loc_1

    lin_regression = stats.linregress(data_subset['Voltage (V)'][index1:index2], cleaned_current[index1:index2])
    background = (lin_regression[0] * data_subset['Voltage (V)']) + lin_regression[1]
    correction_vals = np.zeros(len(background))
    index = 0
    for val in background:
        correction_vals[index] = (0 - val)
        index += 1
    corrected_current = cleaned_current + correction_vals
    return(corrected_current)


def background_zero(current_data):
    minimum_current = np.min(current_data)
    zeroed_current = current_data - minimum_current
    return zeroed_current


def get_id(id_potential, data):
    id_val = data.loc[data['Voltage (V)'] == id_potential, 'Zeroed Current (pA)']
    id_current = data['Zeroed Current (pA)'] / id_val.values[0]
    data['Normalized Current (pA)'] = id_current
    return(data)


def rounding(value):
    value = np.multiply(value, 1000) # conversion to mV
    double = np.multiply(value, 2)
    division = np.divide(double, 2)
    rounded = np.round(division, 1)
    return rounded

    
def current_quartiles(data, redox_event):

    if redox_event:
        half_quart = 0.5
        three_quarter_quart = 0.75 # why? because this approximation was formed for a reduction event - I want to study oxidation events, so my 3/4 current is essentially inverted
        quarter_quart = 0.25 # Inverse of explanation in previous comment
        try:
            half_loc = data.loc[round(data['Normalized Current (pA)'], 2) == half_quart, 'Voltage (V)'].values[0]
            quarter_loc = data.loc[round(data['Normalized Current (pA)'], 2) == quarter_quart, 'Voltage (V)'].values[0]
            three_quarter_loc = data.loc[round(data['Normalized Current (pA)'], 2) == three_quarter_quart, 'Voltage (V)'].values[0]
            return(half_loc, quarter_loc, three_quarter_loc)
        except IndexError:
            half_loc = np.nan
            quarter_loc = np.nan
            three_quarter_loc = np.nan
            return(half_loc, quarter_loc, three_quarter_loc)

    else:
        half_quart = 0.5
        three_quarter_quart = 0.25 # why? because this approximation was formed for a reduction event - I want to study oxidation events, so my 3/4 current is essentially inverted
        quarter_quart = 0.75 # Inverse of explanation in previous comment
        try:
            half_loc = data.loc[round(data['Normalized Current (pA)'], 2) == half_quart, 'Voltage (V)'].values[0]
            quarter_loc = data.loc[round(data['Normalized Current (pA)'], 2) == quarter_quart, 'Voltage (V)'].values[0]
            three_quarter_loc = data.loc[round(data['Normalized Current (pA)'], 2) == three_quarter_quart, 'Voltage (V)'].values[0]
            return(half_loc, quarter_loc, three_quarter_loc)
        except IndexError:
            half_loc = np.nan
            quarter_loc = np.nan
            three_quarter_loc = np.nan
            return(half_loc, quarter_loc, three_quarter_loc)


if __name__ == "__main__":
    main()

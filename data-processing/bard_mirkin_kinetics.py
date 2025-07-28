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
    linear_region = [0.04, 0.0] # Defining start and end of linear region for background correction
    formal_potential = 0.4 # V, formal redox potential of probe
    id_potential = 0.0 # V, potential where diffusion-limited current is observed
    diffusion_coef = 1 * (10 ** -6) # cm2/s
    tip_radius = 2.5 * (10 **-5) #cm
    potential_range = [0.6, -0.1] # V!
    sweep_number = 2
    goofy_format = True # This is for when the SECCM is configured to record currents in US convention, thus making the potentials backward. Hopefully will be fixed in a future update of the SECCM software.

    # working parts of code
    data_path = r"E:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\data\01Nov2024_PBTTT_Fc3\scan\0X_0Y_fc_pbttt.csv"
    rate_constant, kappa_naught, kappa_naught_error, transfer_coef, transfer_coef_error, ehalf = get_kinetics(data_path, formal_potential=formal_potential, linear_region=linear_region,  potential_range=potential_range, sweep=sweep_number, diffusion_current_potential=id_potential, diffusion_coefficient=diffusion_coef, tip_radius=tip_radius, goofy_format = goofy_format, plotting=True)
    print(ehalf, rate_constant, kappa_naught, kappa_naught_error, transfer_coef, transfer_coef_error)


def get_kinetics(data_path, formal_potential, linear_region, potential_range, sweep, diffusion_current_potential, diffusion_coefficient, tip_radius, goofy_format, plotting):
    data = pd.read_csv(data_path, sep='\t')

    # This is an important part to consider when updating data output from the SECCM.
    if goofy_format:
        data['Voltage (V)'] *= -1
    else:
        data['Current (pA)'] *= -1

    loc1 = data.loc[data['Voltage (V)'] == potential_range[0]].index   
    loc2 = data.loc[data['Voltage (V)'] == potential_range[1]].index

    if loc1[sweep] < loc2[sweep]:
        data = data[loc1[sweep]:loc2[sweep]]
    else:
        data = data[loc2[sweep]:loc1[sweep]]

    cleaned_current = current_cleanup(data['Current (pA)'])
    corrected_current = background_correction(data, cleaned_current, linear_region[0], linear_region[1]) # deprecated way of correcting current. Skews the trend in my opinion.
    corrected_current = background_zero(corrected_current)
    data['Zeroed Current (pA)'] = corrected_current
    data = data.reset_index(drop=True)
    data = get_id(diffusion_current_potential, data)
    h, q, tq = current_quartiles(data) # q, h, tq = quarter, half, threequarter potentials
    # e = data['Voltage (V)']

    try:
        # parameters, covariance = curve_fit(sigmoid_maker_curvefit, (data['Voltage (V)'] - 0.4), data['Normalized Current (pA)'], bounds=([-np.inf, 0],[20,1])) # adding bounds
        parameters, covariance = curve_fit(sigmoid_maker_curvefit, (data['Voltage (V)'] - formal_potential), data['Normalized Current (pA)'])
        approximation_currents = sigmoid_maker_curvefit((data['Voltage (V)'] - formal_potential), parameters[0], parameters[1])
        kappa_naught = parameters[0]
        transfer_coef = parameters[1]
        error_in_fits = np.sqrt(np.diag(covariance))
        kappa_naught_error = error_in_fits[0]
        transfer_coef_error = error_in_fits[1]
        rate_constant = get_rate_constant(diffusion_coefficient, tip_radius, kappa_naught)
        fit_success = True

        ## This section is for saving a particular data set to a CSV file to show the fitting procedure in a conference or something
        
        # save_df = data
        # save_df['Fit Current'] = approximation_currents
        # save_directory = r"dir"
        # save_name = r"name"
        # save_df.to_csv(os.path.join(save_directory,(save_name + ".csv")))


    except RuntimeError:
        "Fit failed."
        kappa_naught = np.nan
        transfer_coef = np.nan
        error_in_fits = np.nan
        kappa_naught_error = np.nan
        transfer_coef_error = np.nan
        rate_constant = np.nan
        approximation_currents = 0
        fit_success = False

    
    if plotting:
        make_plot(data, approximation_currents, q, h, tq, fit_success)
    else:
        print("Analysizing next CV")
        print(data_path)

    return rate_constant, kappa_naught, kappa_naught_error, transfer_coef, transfer_coef_error, h

    
def make_plot(data, approximation_currents, q, h, tq, fit_success):
    plt.rcParams['font.size'] = 14
    fig, ax = plt.subplots()
    # ax.plot(data['Voltage (V)'], data['Current (pA)'], color='purple', label='Raw')
    # ax.plot(data['Voltage (V)'], cleaned_current, color='red', label='Uncorrected')
    # ax.plot(data['Voltage (V)'], corrected_current, color='blue', label='Background corrected')

    ax.plot(data['Voltage (V)'], data['Normalized Current (pA)'], color='purple', label='Normalized')

    if fit_success:
        ax.plot(data['Voltage (V)'], approximation_currents, color='black', label='Fitted', linestyle='--')

    ax.set_xlabel("Potential (V) vs. AgCl")
    ax.set_ylabel("Normalized Current")
    ax.vlines(x =[q, h, tq], ymin=0, ymax=1, color='black', alpha=0.25)
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


def current_quartiles(data):
    half_quart = 0.5
    three_quarter_quart = 0.75 # explanation for this at top of script
    quarter_quart = 0.25 # explanation for this at top of script
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




# all below is not necessary anymore. This approximation was not written for semiconductors and was also formulated for UMEs.

# def alpha_solver(q, h, tq):
#     # debugging vals below
#     # q = 0.42
#     # h = 0.387
#     # tq = 0.357

#     # this is going to solve Equation 24 in the referenced Mirkin Bard paper.
#     faraday = constant.physical_constants['Faraday constant'][0]
#     f = (faraday / (constant.R * 298))
#     n = 1
#     epq = np.exp(n * f * ((q-h)))
#     eptq = np.exp(n * f * ((tq-h)))
#     func = lambda alpha : (np.power(epq, alpha) * (1 - (3*eptq))) + ((3*np.power(eptq, alpha))*(epq - 3)) + (9*eptq) - (epq)
#     alpha_initial_guess = 0.5
#     alpha_solution = fsolve(func, alpha_initial_guess)
#     print(alpha_solution)
#     theta_solver(alpha_solution, epq, eptq)


# def theta_solver(alpha, epq, eptq):
#     print('hello')



if __name__ == "__main__":
    main()

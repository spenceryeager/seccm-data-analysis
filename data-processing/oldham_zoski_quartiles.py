# making the contour plots shown in the Oldham and Zoski paper.
# https://doi.org/10.1016/0022-0728(89)85029-6

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy as sp
from scipy.optimize import fsolve
from scipy import constants


def main():
    save_filepath = r"data-processing\quartile_kappa_alpha_values"
    save_name = r'quartile_vals_large_unabridged'
    alpha_vals = 101
    kappa_vals = 2001

    # single value calculation
    # q = 0.25
    # alpha = 0
    # knaught = 20
    # # equart(q, h[0])
    # h = fsolve(func=lambda h: solve_h(h, knaught, alpha, q), x0=1)
    # print(h)
    # should_be_zero = np.round(solve_h(h, knaught, alpha, q),0)
    # print(should_be_zero)
    # eqmeo = equart(q, h[0])
    # print(eqmeo * 1000)

    # batch calculation, this dataframe will contain all the values.
    q_diff = pd.DataFrame(columns=['Quart 1/4', 'Quart 1/2', 'Quart 3/4', 'Alpha', 'KappaNaught', '1/4 solved h', '1/4 fsolve check (should be zero)','1/2 solved h', '1/2 fsolve check', '3/4 solved h', '3/4 fsolve check', 'dE 1/4 (mV)', 'dE 3/4 (mV)', 'dE 1/2 (mV)', "E1/4 - E 3/4 (mV)"])
    i14 = [] # q value 1/4
    i12 = []
    i34 = [] # q value 3/4
    a_list = [] # transfer coefficient
    kap = [] # kappa naught from the paper
    solved_h_14 = [] # the fsolve derived value of h for q=0.25
    solved_h_12 = [] # ^^^^^ for q = 0.5
    solved_h_34 = [] # ^^^^^ for q = 0.75
    check_val_14 = [] # fsolve check value, should be zero, for q=0.25
    check_val_12 = [] # ^^^^ for q = 0.5
    check_val_34 = [] # ^^^ for q = 0.75 
    e_14 = []
    e_12 = []
    e_34 = []
    dq = [] # the delta of the quartiles

    q = [0.25, 0.5, 0.75]
    alpha = np.linspace(0, 1, alpha_vals)
    knaught = np.linspace(0.2, 20, kappa_vals)
    
    for quartile in q:
        print('Working in quartile ', q)

        for a in alpha:
            print('Solving for alpha ', a)

            for k in knaught:

                if quartile == 0.25:
                    h = fsolve(func=lambda h: solve_h(h, k, a, quartile), x0=5)
                    should_be_zero = np.round(solve_h(h, k, a, quartile),0)
                    eqmeo = 1000 * (equart(quartile, h[0]))
                    i14.append(quartile)
                    a_list.append(a)
                    kap.append(k)
                    solved_h_14.append(h[0])
                    check_val_14.append(should_be_zero[0])
                    e_14.append(eqmeo)
                    # print(quartile)
                    # print(a)
                
                elif quartile == 0.5:
                    h = fsolve(func=lambda h: solve_h(h, k, a, quartile), x0=5)
                    should_be_zero = np.round(solve_h(h, k, a, quartile),0)
                    eqmeo = 1000 * (equart(quartile, h[0]))
                    i12.append(quartile)
                    solved_h_12.append(h[0])
                    check_val_12.append(should_be_zero[0])
                    e_12.append(eqmeo)
                    # print(quartile)

                elif quartile == 0.75:
                    h = fsolve(func=lambda h: solve_h(h, k, a, quartile), x0=5)
                    should_be_zero = np.round(solve_h(h, k, a, quartile),0)
                    eqmeo = 1000 * (equart(quartile, h[0]))
                    i34.append(quartile)
                    solved_h_34.append(h[0])
                    check_val_34.append(should_be_zero[0])
                    e_34.append(eqmeo)

                else: 
                    print('Something went wrong')
                                      

    delta_vals = np.abs(np.subtract(e_14, e_34))

    q_diff['Quart 1/4'] = i14
    q_diff['Quart 1/2'] = i12
    q_diff['Quart 3/4'] = i34
    q_diff['Alpha'] = a_list
    q_diff['KappaNaught'] = kap
    q_diff['1/4 solved h'] = solved_h_14
    q_diff['1/2 solved h'] = solved_h_12
    q_diff['3/4 solved h'] = solved_h_34
    q_diff['1/4 fsolve check (should be zero)'] = check_val_14
    q_diff['1/2 fsolve check'] = check_val_12
    q_diff['3/4 fsolve check'] = check_val_34
    q_diff['dE 1/4 (mV)'] = e_14
    q_diff['dE 1/2 (mV)'] = np.abs(e_12)
    q_diff['dE 3/4 (mV)'] = e_34
    q_diff['E1/4 - E 3/4 (mV)'] = delta_vals
    q_diff.to_csv(os.path.join(save_filepath, (save_name + '.csv')))




def solve_h(h, knaught, alpha, q):
    # this is Equation 18 in the linked paper.
    product = np.divide((2 * knaught), (3 * np.pi * q))
    
    # first alpha exponential, fae
    fae_term1 = np.divide((1 - q), (q))
    fae_term2_num = (2 * (h + 1)) # numerator
    fae_term2_denom = ((3* h)*((2*h) + np.pi))
    fae_term2 = np.divide(fae_term2_num, fae_term2_denom)

    sub_fae = (fae_term1 - fae_term2)
    fae = np.power(sub_fae, alpha)

    # second alpha exponential, sae
    sae_num = 2 * (h + 1)
    sae_denom = (3*h)*((2*h) + np.pi)

    sae = (1 + np.divide(sae_num, sae_denom)) ** (1-alpha)
    
    # return (h * ((np.divide((1 - q), q) - np.divide((2*(h + 1)), (3 * h)*((2*h) + np.pi))) ** alpha) * ((1 + np.divide(2*(h + 1), ((3*h)*(2*h + np.pi)))) ** (1 - alpha))) - product
    
    return ((h * fae * sae) - product)
    

def equart(q, h):
    # This is Equation 19 in the linked paper.
    temp = 298 # K
    inner_log_frac_num = (2 * q) * (h + 1)
    inner_log_frac_denom = (3 * h) * ((2 * h) + np.pi)
    inner_log_frac = np.divide(inner_log_frac_num, inner_log_frac_denom)

    log_term = np.log(np.reciprocal(q + (inner_log_frac)) - 1)

    final_val = np.divide((log_term * temp * constants.R), constants.physical_constants['Faraday constant'][0])

    return final_val

# def equart(q, h):
#     # this is Equation 19 in the linked paper, but rewritten to follow the convention they show of n(Eo - Eq)
#     temp = 298 # K
#     inner_log_frac_num = (2 * q) * (h + 1)
#     inner_log_frac_denom = (3 * h) * ((2 * h) + np.pi)
#     inner_log_frac = np.divide(inner_log_frac_num, inner_log_frac_denom)

#     log_term = np.log((q + (inner_log_frac)) - 1)

#     final_val = np.divide((log_term * temp * constants.R), constants.physical_constants['Faraday constant'][0])

#     return final_val




if __name__ == "__main__":
    main()


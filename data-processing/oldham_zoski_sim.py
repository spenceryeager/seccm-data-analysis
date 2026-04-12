# this is my attempt to model the UME CV. I'm following the description by Oldham and Zoski, here:
# https://doi.org/10.1016/0022-0728(89)85029-6

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as constant


def main():
    # constants
    do = 4.1 * (10 ** -6) # cm2 / s, diffusion coefficient
    dr = do # we assume the diffusion of the redox probe is the same in the oxidized and reduced state
    n = 1 # number of electrons transfered
    a = 2.7 * (10 **-5) # radius of tip, in cm 
    eo = 0 # formal potential
    e = np.linspace(-1, 1, 1000) # potential range
    # e = e - eo
    # ko = 0.2 # actual rate coefficient, in cm / s
    kappanaught = 20
    transfer_coef = 0.4 # transfer coefficient
    reduction = False # are we looking at a reduction process or an oxidation process?
    val = sigmoid_maker(do, dr, n, a, e, eo, kappanaught, transfer_coef, reduction)
    fig, ax = plt.subplots()
    ax.plot(e, val)
    ax.set_xlabel("Overpotential (V)")
    ax.set_ylabel("Normalized Current")
    ax.set_xlim(-0.2, 0.4)
    ax.invert_xaxis()
    plt.show()


def sigmoid_maker(do, dr, n, a, e, eo, kappanaught, transfer_coef, reduction):
    # kappanaught = rate_to_kap(ko=ko, do=do, a=a)
    theta = theta_calc(do, dr, n, e, eo, reduction)
    kappa = kappa_calc(kappanaught, transfer_coef, n, e, eo, reduction)
    val = current_potential_relation(theta, kappa)
    
    
    if not reduction:
        val = np.negative(val)
    

    return val

def sigmoid_maker_curvefit(e, ko, transfer_coef):
    # this function only relies on x vals, ko, and transfer_coef for compatibility with scipy's curve fit.
    dr = 1
    do = 1
    n = 1
    theta = theta_calc(do, dr, n, e)
    kappa = kappa_calc(ko, transfer_coef, n, e)
    val = current_potential_relation(theta, kappa)
    return val

    

def theta_calc(do, dr, n, e, eo, reduction):
    temp = 298
    F = constant.physical_constants['Faraday constant'][0]


    if reduction:
        exponential = np.exp((n * F * (e - eo)) / (temp * constant.R)) # for reduction
    else:
        exponential = np.exp(np.negative(n * F * (e - eo)) / (temp * constant.R)) # for oxidation
    

    theta_val = 1 + (do/dr) * exponential
    return(theta_val)


def kappa_calc(kappanaught, transfer_coef, n, e, eo, reduction):
    temp = 298
    F = constant.physical_constants['Faraday constant'][0]

    if reduction:
        kappa_val = kappanaught * np.exp(np.negative((n) * (transfer_coef) * F * (e - eo)) / (temp * constant.R)) # This is for reduction
    else:
        kappa_val = kappanaught * np.exp(((n) * (1-transfer_coef) * F * (e - eo)) / (temp * constant.R)) # This is for oxidation

    return(kappa_val)


def rate_to_kap(ko, do, a):
    kappanaught = (np.pi * ko * a) / (4*do)
    print(kappanaught)
    return kappanaught


def current_potential_relation(theta, kappa):
    # this is equation 13 in top paper. Going to break up most of it to make it easier to follow...
    kappatheta = theta * kappa
    numerator1 = (2 * kappatheta) + (3 * constant.pi)
    denominator1 = (4 * kappatheta) + (3 * constant.pi ** 2)
    fraction1 = numerator1 / denominator1
    
    numerator2 = constant.pi
    denominator2 = kappatheta
    fraction2 = numerator2 / denominator2
    product1 = fraction2 * fraction1
    inverse = np.reciprocal((1 + product1))
    final_product = np.reciprocal(theta) * inverse
    return final_product
    


if __name__ == "__main__":
    main()
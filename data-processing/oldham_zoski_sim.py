# this is my attempt to model the UME CV. I'm following the description by Oldham and Zoski, here:
# https://doi.org/10.1016/0022-0728(89)85029-6

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as constant


def main():
    # constants
    do = 1 * (10 **-5)
    dr = 1 * (10 **-5)
    n = 1
    eo = 0.4
    e = np.linspace(-0.2, 0.8, 100)
    e = e - eo
    ko = 0.003
    transfer_coef = 0.89
    val = sigmoid_maker(do, dr, n, e, ko, transfer_coef)
    fig, ax = plt.subplots()
    ax.plot(e, val)
    ax.set_xlabel("Potential (V)")
    ax.set_ylabel("Normalized Current")
    ax.invert_xaxis()
    plt.show()


def sigmoid_maker(do, dr, n, e, ko, transfer_coef):
    theta = theta_calc(do, dr, n, e)
    kappa = kappa_calc(ko, transfer_coef, n, e)
    val = current_potential_relation(theta, kappa)
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

    

def theta_calc(do, dr, n, e):
    temp = 298
    F = constant.physical_constants['Faraday constant'][0]
    exponential = np.exp((n * F * (e)) / (temp * constant.R))
    theta_val = 1 + (do/dr) * exponential
    return(theta_val)


def kappa_calc(ko, transfer_coef, n, e):
    temp = 298
    F = constant.physical_constants['Faraday constant'][0]
    kappa_val = ko * np.exp(((- n) * transfer_coef * F * (e)) / (temp * constant.R))
    return(kappa_val)


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
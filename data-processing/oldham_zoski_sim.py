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
    e = np.linspace(-0.2, 0.8, 50)
    print(e)
    ko = 0.003
    transfer_coef = 0.89
    theta = theta_calc(do, dr, n, eo, e)
    kappa = kappa_calc(ko, transfer_coef, n, e, eo)
    val = current_potential_relation(theta, kappa)
    print(val)
    fig, ax = plt.subplots()
    ax.plot(e, val)
    plt.show()

    

def theta_calc(do, dr, n, eo, e):
    temp = 298
    F = constant.physical_constants['Faraday constant'][0]
    exponential = np.exp((n * F * (e - eo)) / (temp * constant.R))
    theta_val = 1 + (do/dr) * exponential
    return(theta_val)


def kappa_calc(ko, transfer_coef, n, e, eo):
    temp = 298
    F = constant.physical_constants['Faraday constant'][0]
    kappa_val = ko * np.exp(((- n) * transfer_coef * F * (e - eo)) / (temp * constant.R))
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
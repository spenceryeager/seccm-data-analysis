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
    ko = 1
    transfer_coef = 0.5
    theta(do, dr, n, eo, e)
    # kappa(ko, transfer_coef, n, e, eo)
    

def theta(do, dr, n, eo, e):
    temp = 298
    F = constant.physical_constants['Faraday constant'][0]
    exponential = np.exp((n * F * (e - eo)) / (temp * constant.R))
    print(exponential)


def kappa(ko, transfer_coef, n, e, eo):
    temp = 298
    F = constant.physical_constants['Faraday constant'][0]
    kappa_val = ko * np.exp(((- n) * transfer_coef * F * (e - eo)) / (temp * constant.R))
    print(kappa_val)


if __name__ == "__main__":
    main()
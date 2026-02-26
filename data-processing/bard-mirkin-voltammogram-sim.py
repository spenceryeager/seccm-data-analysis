# Simulating a quasi-reversible steady-state non-uniformly accessible (microdisk) electrode voltammogram
# the equations from this can be found in this DOI:
# equations 28, 29, and 7. 

import numpy as np
import os
import scipy as sp
import scipy.constants as constant


def main():
    f = f_constant(298) # consolidated f, where f = F/RT
    n = 1 # number of electrons
    d = 500 * 10**-7 # cm, diameter of the tip


def f_constant(temp):
    faraday = constant.physical_constants['Faraday constant'][0]
    r_const = constant.physical_constants['molar gas constant'][0]
    f = np.divide(faraday, (np.multiply(r_const, temp)))
    return f


def theta(do, dr, eo, e, f, n):
    theta = 1 + ((np.divide(do, dr)) * np.exp(n * f * (e - eo)))
    return theta


def kprime(do, d, n, f, e, eo):
    return 1
    

if __name__ == '__main__':
    main()

    
    
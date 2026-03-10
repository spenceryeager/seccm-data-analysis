# making the contour plots shown in the Oldham and Zoski paper.
# https://doi.org/10.1016/0022-0728(89)85029-6

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp
from scipy.optimize import fsolve


def main():
    # q = [0.25, 0.5, 0.75]
    # alpha = np.linspace(0, 1, 101)
    # knaught = np.linspace(0.2, 20, 201)
    q = 0.25
    alpha = 0.5
    knaught = 1
    h = fsolve(func=lambda h: solve_h(h, knaught, alpha, q), x0=1)
    print(h)
    should_be_zero = np.round(solve_h(h, knaught, alpha, q),0)
    print(should_be_zero)


def solve_h(h, knaught, alpha, q):
    # this is Equation 18 in the linked paper.
    product = np.divide((2 * knaught), (3 * np.pi * q))
    
    # first alpha exponential, fae
    fae_term1 = np.divide((1 - q), (q))
    fae_term2_num = (2 * (h + 1)) # numerator
    fae_term2_denom = ((3* h)*((2*h) + np.pi))
    fae_term2 = np.divide(fae_term2_num, fae_term2_denom)

    fae = (fae_term1 - fae_term2) ** alpha

    # second alpha exponential, sae
    sae_num = 2 * (h + 1)
    sae_denom = (3*h)*((2*h) + np.pi)

    sae = (1 + np.divide(sae_num, sae_denom)) ** (1-alpha)
    
    # return (h * ((np.divide((1 - q), q) - np.divide((2*(h + 1)), (3 * h)*((2*h) + np.pi))) ** alpha) * ((1 + np.divide(2*(h + 1), ((3*h)*(2*h + np.pi)))) ** (1 - alpha))) - product
    
    return (h * fae * sae) - product
    








if __name__ == "__main__":
    main()


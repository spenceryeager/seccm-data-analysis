# using this program to simulate sigmoids with the goal of eventually fitting experimental data
# Following this paper: https://doi.org/10.1021/acs.jpcc.9b10367

import numpy as np
import scipy.constants as const
import matplotlib.pyplot as plt


def main():
    straight_sig()


def straight_sig():
    a = 1
    b = 1
    x_vals = np.arange(-10, 10, 0.5)
    y_vals = (1 / (1 + np.exp(np.negative(a) * (x_vals - b))))
    print(y_vals)
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals)
    plt.show()


def ss_ume_approx():
    currents = [0]
    # this approximation comes from ref 25 in above paper, https://doi.org/10.1016/0022-0728(88)80060-3
    diffusion_coef_red = 1 # diffusion coefficient of reduced species
    diff_coef_ox = 1 # diffusion coefficient of oxidized species
    electrode_radius = 500 # nm, need to confirm this
    kf = 1 # forward rate constant
    kb = 1 # backward rate constant


def capacitances():
    # constants
    e_int = 3.5
    e_solv = 64.9
    helmholtz_thickness = 0.233 # nm?
    ionic_strength = 0.05 # mol/L, paper says concentration can be used here
    temp = 273

    cap_h = (e_int + const.epsilon_0) / helmholtz_thickness # equation 7 in paper
    cap_dl = np.sqrt((2 * e_solv * const.epsilon_0 * const.elementary_charge * ionic_strength) / (const.Boltzmann * temp)) # equation 8 approximation in paper
    cap_sc = 1
    print(cap_h)


if __name__ == "__main__":
    main()
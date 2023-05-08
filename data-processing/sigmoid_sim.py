# using this program to simulate sigmoids with the goal of eventually fitting experimental data
# Following this paper: https://doi.org/10.1021/acs.jpcc.9b10367

import numpy as np
import scipy.constants as const


def main():
    capacitances()


def capacitances():
    e_int = 1
    e_solv = 3
    helmholtz_thickness = 1
    cap_h = (e_int + const.epsilon_0) / helmholtz_thickness # equation 7 in paper
    cap_dl = np.sqrt((2 * e_solv * const.epsilon_0 * ))
    # equation 8 approximation in paper


    print(cap_h)


if __name__ == "__main__":
    main()
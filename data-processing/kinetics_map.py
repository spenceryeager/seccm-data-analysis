# this turns the kinetics histogram into a map instead of a distribution

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
    filepath = r"C:\Users\Spencer\Documents\data-analysis\28Mar2023_PBTTT_Fc\analysis\results_with_bounds_pbttt.csv"
    data_file = pd.read_csv(filepath)
    print(data_file)

    unique_x = list(set(data_file['X (um)']))
    unique_y = list(set(data_file['Y (um)']))
    X, Y = np.meshgrid(unique_x, unique_y)
    Z_kinetics = data_file.pivot_table(index="X (um)", columns="Y (um)", values="log10 Rate Constant").T.values

    make_plot(X, Y, Z_kinetics)


def make_plot(X, Y, Z_current):
    font = {'size': 18}
    plt.rc('font', **font)
    fig, ax = plt.subplots(tight_layout=True)
    im = ax.pcolormesh(X, Y, Z_current,vmin=-4, vmax=-2)
    ax.set_xlabel('X ($\\rm\mu$m)')
    ax.set_ylabel('Y ($\\rm\mu$m)')
    cb = fig.colorbar(im, ax=ax)
    cb.set_label('log$_{10}$ k$_{0}$')
    ax.set_title("PBTTT")
    plt.show()


if __name__ == "__main__":
    main()

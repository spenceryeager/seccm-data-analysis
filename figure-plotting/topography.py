# This is used to convert the recorded (x, y, z) data into a topography map

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from matplotlib import rcParams
import os
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'
rcParams['savefig.dpi'] = 300


def main():
    make_topography()


def make_topography():
    filepath = r"E:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\data\SECCM_Data\04June2026_p3ht_colocation\Fc\scan\position-data\position-data.csv"
    top_data = pd.read_csv(filepath, sep='\t')
    # print(top_data.head())
    Z = top_data.pivot_table(index='X Command (um)',
                            columns='Y Command (um)',
                            values='Z Extension (um)').T.values

    x_vals = top_data['X Command (um)'].unique()
    y_vals = top_data['Y Command (um)'].unique()
    x_grid, y_grid = make_grid(x_vals, y_vals)
    
    # Setting font size before making plot
    fontsize = 35
    mpl.rcParams.update({'font.size': fontsize, 'figure.autolayout': True})

    # creating plot
    fig, ax = plt.subplots(figsize=(10,10), tight_layout=True)    
    im = ax.pcolormesh(x_grid, y_grid, Z)

    # Graph properties
    ax.set_xlabel('X ($\\rm\mu$m)')
    ax.set_ylabel('Y ($\\rm\mu$m)')
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label('Z Extension ($\\rm\mu$m)')
    cb.outline.set_linewidth(3)
    ax.xaxis.labelpad = 5
    ax.yaxis.labelpad = 5
    # ax.minorticks_on()
    # ax.tick_params(axis = 'both', direction='in', which='major', length=9, width=3)
    # ax.tick_params(axis = 'both', direction='in', which='minor', length=4.5, width=3)

    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3)
    
    ax.set_box_aspect(1)
    plt.show()

def make_grid(x_data, y_data):
    X, Y = np.meshgrid(x_data, y_data)
    return(X, Y)


if __name__ == '__main__':
    main()
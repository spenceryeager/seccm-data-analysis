# This is used to convert the recorded (x, y, z) data into a topography map

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    make_topography()


def make_topography():
    filepath = r"dir"
    top_data = pd.read_csv(filepath, sep='\t')
    # print(top_data.head())
    Z = top_data.pivot_table(index='X Command (um)',
                            columns='Y Command (um)',
                            values='Z Extension (um)').T.values

    x_vals = top_data['X Command (um)'].unique()
    y_vals = top_data['Y Command (um)'].unique()
    x_grid, y_grid = make_grid(x_vals, y_vals)
    
    fig, ax = plt.subplots()
    im = ax.pcolormesh(x_grid, y_grid, Z)

    # Graph properties
    ax.set_xlabel('X ($\\rm\mu$m)')
    ax.set_ylabel('Y ($\\rm\mu$m)')
    cb = fig.colorbar(im, ax=ax)
    cb.set_label('Z Extension ($\\rm\mu$m)')
    plt.show()

def make_grid(x_data, y_data):
    X, Y = np.meshgrid(x_data, y_data)
    return(X, Y)


if __name__ == '__main__':
    main()
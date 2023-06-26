# this can be used to make a representational map of the scan area

import numpy as np
import matplotlib.pyplot as plt


def main():
    x_length = 20 # um, enter length in x direction in um 
    y_length = 20 # um, enter length in y direction in um
    x_step = 1 # um, enter step length in the x direction in um
    y_step = 1 # um, enter step length in the y direction in um
    make_map(x_length, y_length, x_step, y_step)


def make_map(x_length, y_length, x_step, y_step):
    # This is making the interval length. Adding 1 because counting starts at 0.
    x_intervals = int(x_length+1 / x_step)
    y_intervals = int(y_length+1 / y_step)
    x_vals = np.linspace(0, x_length, x_intervals)
    y_vals = np.linspace(0, y_length, y_intervals)
    X, Y = np.meshgrid(x_vals, y_vals)
    
    fig, ax = plt.subplots()
    ax.scatter(X, Y, marker="x", color='red')
    ax.set_xlabel("$\mu$m")
    ax.set_ylabel("$\mu$m")
    ax.set_title("Scan Area")
    plt.show()


if __name__ == "__main__":
    main()
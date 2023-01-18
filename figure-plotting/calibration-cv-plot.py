import matplotlib.pyplot as plt
import pandas as pd


def main():
    display_plot()


def display_plot():
    # Setting font size before making plot
    font = {'size': 12}
    plt.rc('font', **font)

    fc_redox_correction = 0.5

    # Data loading
    initial_scan_loc = r"dir"
    initial_data = pd.read_csv(initial_scan_loc,
                                sep = '\t')
    final_scan_loc = r"dir"
    final_data = pd.read_csv(final_scan_loc,
                                sep = '\t')
    v = 'Voltage (V)' # file headers
    i = 'Current (pA)'

    # Plotting
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(initial_data[v], initial_data[i] * -1, 
            color='red', 
            label='Initial Scan')

    ax.plot(final_data[v], final_data[i] * -1,
            color='purple',
            label='Final Scan')
    
    # Secondary axis
    ax2 = ax.secondary_xaxis("top", functions=(lambda x: x-fc_redox_correction, lambda x: x+fc_redox_correction))
    ax2.minorticks_on()

    # Formatting plot
    ax.set_xlabel('Potential vs. Ag Wire (V)')
    ax2.set_xlabel('Potential vs. Fc/Fc$^{+}$ (V)')
    ax.set_ylabel('Current (pA)')
    ax.invert_xaxis()
    ax.minorticks_on()
    ax.legend()

    # display
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
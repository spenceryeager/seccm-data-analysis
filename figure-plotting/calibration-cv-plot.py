import matplotlib.pyplot as plt
import pandas as pd


def main():
    display_plot()


def display_plot():
    # Data loading
    initial_scan_loc = 'enter filepath'
    initial_data = pd.read_csv(data_location)
    final_scan_loc = 'enter filepath'
    final_data = pd.read_csv(final_scan_loc)
    v = 'Voltage (V)' # file headers
    i = 'Current (pA)'

    # Plotting
    fig, ax = plt.subplots()
    ax.plot(initial_data[v], initial_data[i], 
            color='red', 
            label='Initial Scan')

    ax.plot(final_data[v], final_data[i],
            color='blue',
            label='Final Scan')
    
    ax.set_xlabel('Potential vs. Ag Wire')
    ax.set_ylabel('Current (pA)')
    ax.legend()
    plt.show


if __name__ == '__main__':
    main()
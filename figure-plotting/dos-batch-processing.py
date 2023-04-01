# batch file for calculating DOS from all SECCM runs.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from dos_calculation import dos_array_return
from directory_sorting import directory_sort


def main():
    data_directory = r"C:\Users\spenceryeager\Documents\seccm-data\19Mar2023_rrP3HT_500nm-tip\scan1"
    file_list = []
    sorted_file_list = directory_sort(data_directory)
    print(sorted_file_list)



if __name__ == "__main__":
    main()

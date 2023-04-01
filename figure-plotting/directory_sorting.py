# this file will sort the directory based on the initial "x_Y_" file name.

import os


def main():
    directory_sort()


def directory_sort(dir_path):
    data_list = []
    for item in os.listdir(dir_path):
        if item.endswith('.csv'):
            data_list.append(item)
    sorted_file_list = sorted(data_list, key=lambda x: [[int(x.split("_")[1][:-1])], [int(x.split("_")[0][:-1])]])
    # the above is a mouthful. This is sorting based on the X and Y value. lambda x here can be thought of as the item in the list. it is then split at the "_"
    # since this is the separator between the numbers. Indices 0 and 1 are the "numX" and "numY", the [:-1] removes the "X" and "Y" from the string. It's all
    # then converted to an int.
    full_path_list = []
    for fname in sorted_file_list:
        full_path_list.append(os.path.join(dir_path, fname))
    return full_path_list


if __name__ == "__main__":
    main()

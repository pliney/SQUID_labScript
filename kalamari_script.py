from pprint import pprint as pp
import csv
import numpy as np
import sys
import ntpath
import os
if sys.version_info[0] >= 3:
    from tkinter.filedialog import askdirectory, askopenfilename
    from tkinter import messagebox
if sys.version_info[0] < 3:
    from tkFileDialog import askopenfilename, askdirectory
    import tkMessageBox as messagebox
    import tkSimpleDialog

"""If the format of the header generated in kalamari changes then update this string to match the first couple entries"""
default_header = "I_Flux, I_Bias"

"""If the number of bias steps used in kalamari changes update this value"""
default_bias_steps = 3

default_save_dir = '/Volumes/Users/Shared/'#Kalamari Noise Files/"'

default_load_dir = '/Users/slintern/Documents/'#Labview%20Data/'


def get_data_from_file(filename, header_string=default_header):
    """
    Reads a kallamari noise file and extracts the data, removing the headers. Returns a list in which each line is one
    row of data from the noise file.
    :param filename: Name of file to be read, path is either relative to current location or an absolute path can be given
    :param header_string: A string containing the start of the header row from the data file. This is used to determine
    where the data entries start. If these headers are changed at some point in the future this will need to be updated.
    :return: A list in which each entry contains one row of data from the noise file.
    """

    data = []
    with open(filename, 'r') as f:

        #Read the entire file into one string
        file_data = f.read()

        #Splits the data file into lines
        file_data = file_data.splitlines()

        next_index = 0
        nextline = file_data[next_index]
        #Reads through the data file one line at a time until it find the header line
        while not nextline.startswith(header_string):
            next_index += 1
            nextline = file_data[next_index]

        #Creates a list of all lines in the file after the header line.
        data = file_data[next_index+1:]

    return data

def add_headers(matrix, bias_step, headerstring='I_Flux, I_Bias, Voltage, dV/dI F(), Rd(), Sv, Si'):
    next_headers = [header.strip() for header in headerstring.split(',')]
    next_headers = np.transpose(np.array([[header + str(bias_step)] for header in next_headers]))

    return (np.concatenate((next_headers, matrix),0))

def format_data(data_matrix, num_steps, num_bias_steps=default_bias_steps):
    """

    :param data_matrix: A 2d array containing the data values from noise file
    :param num_steps: Number of flux steps
    :param num_bias: Number of bias steps
    :return: A formatted 2d numpy array with the data from each bias step separated into separate columns, headers have
            also been added to the top of each column.
    """
    #Separates each line into separate data entries and removes whitespace
    split_matrix = [line.strip().replace(' ', '').split(',') for line in data_matrix]

    # determines the number of data columns
    num_columns = len(split_matrix[0])

    np_matrix = np.asarray(split_matrix)

    #Seperates data from the first bias step from the rest of the data
    formatted_data = np_matrix[0:num_steps, 0:num_columns]

    #Adds headers to data
    formatted_data = add_headers(formatted_data,1)

    #Combines the data from all bias steps one at a time
    for i in range(1,num_bias_steps+1):
        next_set = np_matrix[i*num_steps:(i+1)*num_steps, 0:num_columns]
        next_set = add_headers(next_set, i+1)
        formatted_data = np.concatenate((formatted_data, next_set), 1)

    return formatted_data


def get_data_filename():
    messagebox.showinfo(message="Select noise file")
    return askopenfilename(title="Select noise file", initialdir=default_load_dir)


def get_save_filename(data_file_fullpath):
    filename = ntpath.basename(data_file_fullpath) + '.csv'
    messagebox.showinfo(message="Select directory where the formatted csv will be saved")
    save_dir = askdirectory(title="Select save directory", initialdir=default_save_dir)
    return os.path.join(save_dir, filename)


def get_num_flux_steps():
    flux_steps = tkSimpleDialog.askstring("", "Enter the number of flux steps:", initialvalue='60')
    try:
        int(flux_steps)
    except ValueError:
        raise ValueError('Invalid input. Number of steps must be an integer')
    return int(flux_steps)


def save_csv(filename, processed_data):
    np.savetxt(filename, processed_data, fmt='%s', delimiter=', ')
    print('Formatted csv saved to: ' + filename)


def main():
    noise_filename = get_data_filename()
    save_dir = get_save_filename(noise_filename)

    file_data = get_data_from_file(noise_filename)
    num_steps = get_num_flux_steps()
    processed_data = format_data(file_data, num_steps)
    save_csv(save_dir, processed_data)


if __name__ == "__main__":
    main()

from pprint import pprint as pp
import csv
import numpy as np

def get_data_from_file(filename, header_string = "I_Flux, I_Bias"):
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

        #The noise files use return characters instead of newlines so the entire file is read as one line
        file_data = f.read()

        #Splits the data file into lines using return characters
        file_data = file_data.splitlines()
        # file_data = file_data.split("\r")


        next_index = 0
        nextline = file_data[next_index]
        #Reads through the data file one line at a time until it find the header line
        while not nextline.startswith(header_string):
            next_index += 1
            nextline = file_data[next_index]

        #Creates a list of all lines in the file after the header line.
        data = file_data[next_index+1:]
        #
        # #Skip past first few lines of irrelevant information
        # for i in range(0,skip_lines):
        #     f.readline()

    return data

def add_headers(matrix, bias_step, headerstring='I_Flux, I_Bias, Voltage, dV/dI F(), Rd(), Sv, Si'):
    next_headers = [header.strip() for header in headerstring.split(',')]
    next_headers = np.transpose(np.array([[header + str(bias_step)] for header in next_headers]))

    return (np.concatenate((next_headers, matrix),0))

def format_data(data_matrix, num_steps, num_bias_steps=3):
    """

    :param data_matrix: A 2d array containing the data values from noise file
    :param num_steps: Number of flux steps
    :param num_bias: Number of bias steps
    :return: A formatted 2d numpy array with the data from each bias step seperated into seperate columns, headers have
            also been added to the top of each column.
    """
    #Seperates each line into seperate data entries and removes whitespace
    split_matrix = [line.strip().replace(' ', '').split(',') for line in data_matrix]

    # determines the number of data columns
    num_columns = len(split_matrix[0])

    np_matrix = np.asarray(split_matrix)

    #Seperates data from the first bias step from the rest of the data
    formatted_data = np_matrix[0:num_steps, 0:num_columns]

    #Adds headers to data
    formatted_data = add_headers(formatted_data,1)

    #Combines the data from all bias steps one at a time
    for i in range(0,num_bias_steps):
        next_set = np_matrix[i*num_steps:(i+1)*num_steps, 0:num_columns]
        next_set = add_headers(next_set, i+2)
        formatted_data = np.concatenate((formatted_data, next_set),1)

    return formatted_data


def get_data_filename():
    return 'W34R4C7'


def get_save_dir():
    return 'test2.csv'


def get_num_flux_steps():
    return 60


def save_csv(filename, processed_data):
    np.savetxt(filename, processed_data, fmt='%s', delimiter=', ')


def main():
    noise_filename=get_data_filename()
    save_dir = get_save_dir()
    num_steps = get_num_flux_steps()
    num_bias_steps = 3

    file_data = get_data_from_file(noise_filename)
    num_steps = get_num_flux_steps()
    processed_data = format_data(file_data, num_steps)
    save_csv(save_dir, processed_data)


if __name__ == "__main__":
    main()

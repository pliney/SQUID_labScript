from pprint import pprint as pp
import csv
import numpy as np

def get_data_from_file(filename, header_string = "I_Flux, I_Bias"):
    """
    Reads a kallamari noise file and extracts the data, remoing the headers. Returns a list in which each line is one
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


def format_data(data_matrix, num_steps, num_bias_steps=3,):
    """

    :param data_matrix:
    :param num_steps:
    :param num_bias:
    :return:
    """
    #Seperates each line into seperate data entries and removes whitespace
    split_matrix = [line.strip().replace(' ', '').split(',') for line in data_matrix]

    # determines the number of data columns
    num_columns = len(split_matrix[0])

    np_matrix = np.asarray(split_matrix)

    #Seperates data from the first bias step from the rest of the data
    formatted_data = np_matrix[0:num_steps, 0:num_columns]

    #Combines the data from all bias steps one at a time
    for i in range(0,num_bias_steps):
        next_set = np_matrix[i*num_steps:(i+1)*num_steps, 0:num_columns]
        formatted_data = np.concatenate((formatted_data, next_set),1)

    return formatted_data


def get_data_dir():
    return ''


def get_save_dir():
    return ''


def save_csv(filename, processed_data, num_bias_steps, headerstring='I_Flux, I_Bias, Voltage, dV/dI F(), Rd(), Sv, Si'):
    headers = (headerstring+',')*(num_bias_steps) + headerstring
    np.savetxt(filename, processed_data, fmt='%s', delimiter=',', header=headers, comments='')


def get_num_steps():
    pass


def main():
    get_data_dir()
    get_save_dir()
    num_steps = get_num_steps()


if __name__ == "__main__":
    num_bias_steps = 3

    file_data = get_data_from_file("W34R4C7")
    processed_data = format_data(file_data, 60)
    save_csv('test.csv',processed_data, num_bias_steps)

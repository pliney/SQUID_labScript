from pprint import pprint as pp
import csv

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
        file_data = f.readline()

        #Splits the data file into lines using return characters
        file_data = file_data.split("\r")


        next_index = 0
        nextline = file_data[next_index]
        #Reads through the data file one line at a time until it find the header line
        while not nextline.startswith(header_string):
            next_index += 1
            nextline = file_data[next_index]

        #Creates a list of all lines in the file after the header line.
        data = file_data[next_index+1:-1]
        #
        # #Skip past first few lines of irrelevant information
        # for i in range(0,skip_lines):
        #     f.readline()

    pp(data)
    print(len(data))
    return data


def format_data(data_matrix, num_steps, num_bias=4):
    """

    :param data_matrix:
    :param num_steps:
    :param num_bias:
    :return:
    """




def get_data_dir():
    pass


def get_save_dir():
    pass


def save_csv():
    pass


def get_num_steps():
    pass


def main():
    get_data_dir()
    get_save_dir()
    num_steps = get_num_steps()


if __name__ == "__main__":
    # parse_file("MICHAELIM6185")
    get_data_from_file("W34R4C7")
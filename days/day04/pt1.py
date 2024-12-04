import numpy as np
from scipy.signal import convolve2d


def parse_input(input_file):
    with open(input_file, 'r') as file:
        xmas_words = "XMAS".split()

        data = file.readlines()

        # remove the newline character from the end of each line
        data = [line.strip() for line in data]


        # turn the file into a row_count times row_length matrix np.ndarray


def day04_part1(input_file='test.txt'):
    parse_input(input_file)


if __name__ == "__main__":
    day04_part1()

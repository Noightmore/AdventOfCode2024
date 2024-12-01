from typing import List
import gc


def parse_input(file_path: str):
    """
    Reads the input file and returns the data in a suitable format.
    """
    column1: list[int] = []
    column2: list[int] = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():  # Ignore empty lines
                values = line.split()  # Split the line by whitespace
                column1.append(int(values[0]))
                column2.append(int(values[1]))
    return column1, column2


def part1(data):
    """
    Solves part 1 of the day's puzzle.
    """

    list1 = data[0].copy()
    list2 = data[1].copy()
    values = [abs(a - b) for a, b in zip(sorted(list1), sorted(list2))]

    # free memory at data[0] and data[1]
    del data

    summed_value = sum(values)

    return summed_value

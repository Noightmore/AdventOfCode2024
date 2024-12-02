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


def part2(data):
    """
    Solves part 2 of the day's puzzle.
    """
    column1, column2 = data

    # how many times each number from column1 appears in column2
    count = {number: column2.count(number) for number in column1}

    # multiply each number by the number of times it appears in column2 and sum all these numbers
    return sum([number * count[number] for number in count])

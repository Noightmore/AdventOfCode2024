from pathlib import Path
import re

# Regex pattern to match mul(x, y) where x and y are any size numbers
pattern = r"mul\(\d+,\d+\)"


def read_file(path: Path):
    with open(path, 'r') as file:
        return file.readlines()


def get_multiplications(data: list):
    t = 0
    for line in data:
        if re.search(pattern, line):
            matches = re.findall(pattern, line)
            t += sum(
                int(pair[0]) * int(pair[1])
                for match in matches
                for pair in [match[4:-1].split(",")]
            )

    print(t)


def day03_part1():
    path_in = Path(__file__).parent / 'in.txt'
    path_test = Path(__file__).parent / 'test.txt'

    data_in = read_file(path_in)
    data_test = read_file(path_test)

    #print(data_test)
    get_multiplications(data_test)
    #get_multiplications(data_in)


if __name__ == '__main__':
    day03_part1()

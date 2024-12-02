from pathlib import Path


def read_file(path: Path):
    with open(path, 'r') as file:
        return file.readlines()


def day03_part2():
    path_in = Path(__file__).parent / 'in.txt'
    path_test = Path(__file__).parent / 'test.txt'

    data_in = read_file(path_in)
    data_test = read_file(path_in)


if __name__ == '__main__':
    day03_part2()

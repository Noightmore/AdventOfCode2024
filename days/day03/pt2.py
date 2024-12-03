from pathlib import Path
import re


pattern_mul = r"mul\(\d+,\d+\)"
pattern_dos = r"do\(\)"
pattern_dont = r"don't\(\)"


def read_file(path: Path):
    with open(path, 'r') as file:
        return file.readlines()


def get_multiplications(data: list):
    summation = 0
    last_control = None
    for line in data:
        matches_mul = [(match.group(), match.start()) for match in re.finditer(pattern_mul, line)]
        matches_dos = [(match.group(), match.start()) for match in re.finditer(pattern_dos, line)]
        matches_dont = [(match.group(), match.start()) for match in re.finditer(pattern_dont, line)]

        all_matches = sorted(matches_mul + matches_dos + matches_dont, key=lambda x: x[1])
        print(all_matches)



        for match, pos in all_matches:
            if match.startswith("mul"):
                numbers = [int(num) for num in re.findall(r"\d+", match)]
                if last_control is None or last_control == "do()":
                    summation += numbers[0] * numbers[1]
                    print(f"Adding {numbers[0]} * {numbers[1]} = {numbers[0] * numbers[1]}")
            elif match == "do()":
                last_control = "do()"
            elif match == "don't()":
                last_control = "don't()"
                print("Skipping multiplication")
        print(f"Summation: {summation}")
    print(f"Final Summation: {summation}")


def day03_part2():
    path_in = Path(__file__).parent / 'in.txt'
    path_test = Path(__file__).parent / 'test.txt'

    data_in = read_file(path_in)
    data_test = read_file(path_test)

    get_multiplications(data_test)
    get_multiplications(data_in)


if __name__ == '__main__':
    day03_part2() #97728793 187833789
    print(97728793 < 187833789)

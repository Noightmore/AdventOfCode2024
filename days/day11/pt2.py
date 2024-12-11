from functools import cache
from time import perf_counter

import numpy as np

def import_data(input_file='test.txt'):
    with open(input_file, 'r') as file:
        data = file.read().split(' ')
        data = [int(x) for x in data]
    return data  # Return as a regular list for easier iteration


@cache
def count(stone, depth):
    # Every call adds 1 to the count
    counter = 0

    if depth <= 0:
        return 0

    if stone == 0:
        # Recursive call for splitting stone
        counter += count(1, depth - 1)
        return counter

    elif len(str(stone)) % 2 == 0:
        # Split the number in half as a string
        half = len(str(stone)) // 2
        left = int(str(stone)[:half])
        right = int(str(stone)[half:])
        counter += count(left, depth - 1) + count(right, depth - 1)
        counter += 1
        return counter

    # Recursive call for odd-length stones
    counter += count(stone * 2024, depth - 1)

    return counter



def day11_part2():
    stones = import_data('in.txt')

    # Process stones recursively over 75 blinks
    blinks = 75
    total_count = 0

    #for stone in stones:
    #    total_count += count(stone, blinks)

    total_count += sum([count(stone, blinks) for stone in stones])
    total_count += len(stones)

    #total_count += len(stones)
    #total_count += count(1, 2)

    print(total_count)
if __name__ == '__main__':

    time = perf_counter()
    day11_part2() # 277444936413293
    print(perf_counter() - time) # 0.5429236059990217 s

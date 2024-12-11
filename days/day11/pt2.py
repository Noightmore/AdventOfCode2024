import numpy as np
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor, as_completed


def import_data(input_file='test.txt'):
    with open(input_file, 'r') as file:
        data = file.read().split(' ')
        data = [int(x) for x in data]
        data = np.array(data)
    return data


def process_stone(stone):
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        half_len = len(str(stone)) // 2
        divisor = 10 ** half_len
        left = stone // divisor
        right = stone % divisor
        return [left, right]
    else:
        return [stone * 2024]

def update_stones(stones):
    with Pool() as pool:
        results = pool.map(process_stone, stones)
    return np.concatenate(results)



def day11_part1():
    stones = import_data('in.txt')
    print(stones)

    blinks = 75
    for blink in range(blinks):
        stones = update_stones(stones)
        #print(stones)
        print(f"For {blink}th we have stones: {len(stones)}")

    print(len(stones))


if __name__ == '__main__':
    day11_part1()

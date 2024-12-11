import numpy as np


def import_data(input_file='test.txt'):
    with open(input_file, 'r') as file:
        data = file.read().split(' ')
        data = [int(x) for x in data]
        data = np.array(data)
    return data


def update_stones(stones):

    updates_to_apply = []

    for i, stone in enumerate(stones):
        if stone == 0:
            updates_to_apply.append(1)
        elif len(str(stone)) % 2 == 0:
            # split the number in half as string
            half = len(str(stone)) // 2
            left = str(stone)[:half]
            right = str(stone)[half:]

            updates_to_apply.append(int(left))
            updates_to_apply.append(int(right))
        else:
            stone *= 2024
            updates_to_apply.append(stone)

    # redefine stones array based on updates, where for each item in updates is a tuple with index
    # where the new item should be placed and the new value
    stones = np.array(updates_to_apply)
    return stones

def day11_part1():
    stones = import_data('in.txt')
    print(stones)

    blinks = 75
    for _ in range(blinks):
        stones = update_stones(stones)
        print(stones)

    print(len(stones))


if __name__ == '__main__':
    day11_part1()

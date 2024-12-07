import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def load_file(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()

    lines = [line.strip() for line in data]

    vals = {}
    for line in lines:
        # Split at ':'
        left, right = line.split(':')
        key = int(left.strip())
        # Split the right part into numbers
        values = list(map(int, right.strip().split()))
        vals[key] = np.array(values)

    return vals


def can_make_target(target, numbers):
    # If no numbers, can't make target
    if len(numbers) == 0:
        return False

    # If there's only one number, just check equality
    if len(numbers) == 1:
        return numbers[0] == target

    # Start from the first number and proceed in order without rearranging
    return ordered_dfs(target, numbers, 1, numbers[0])


def ordered_dfs(target, numbers, index, current_value):
    # If we've used all numbers, check if we reached the target
    if index == len(numbers):
        return current_value == target

    next_num = numbers[index]

    # Try addition
    if ordered_dfs(target, numbers, index + 1, current_value + next_num):
        return True

    # Try multiplication
    if ordered_dfs(target, numbers, index + 1, current_value * next_num):
        return True

    # Optional: subtraction
    #if ordered_dfs(target, numbers, index + 1, current_value - next_num):
    #    return True

    # Optional: division (check for zero)
    #if next_num != 0 and ordered_dfs(target, numbers, index + 1, current_value / next_num):
    #    return True

    return False


def process_entry(target, values):
    result = can_make_target(target, values)
    return target, result


def day07_part1(data_dict):
    t = 0
    # Use a thread pool with 16 workers
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = []
        for target, values in data_dict.items():
            futures.append(executor.submit(process_entry, target, values))

        for future in as_completed(futures):
            target, result = future.result()
            print(f"Target {target}, numbers {data_dict[target]}: {'Possible' if result else 'Not possible'}")
            if result:
                t += target
    return t


if __name__ == '__main__':
    start = time.time()
    numbers = load_file('in.txt')
    print(numbers)
    total = day07_part1(numbers)
    print("Sum of all possible targets:", total)
    print(f"Execution Time: {time.time() - start} seconds") # for test data: Execution Time: 0.0018315315246582031 seconds

    # Sum of all possible targets: 1298300079253
    # Execution Time: 103.18761444091797 seconds

    # 1298300076754, time: 0.18009257316589355 seconds
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def load_file(file_path):
    """
    Loads the input file and parses it into a dictionary.
    Each key is the first number of a line, and the value is a NumPy array of the subsequent numbers.

    Example:
        Input Line: "190: 10 19"
        Parsed as: {190: np.array([10, 19])}
    """
    with open(file_path, 'r') as file:
        data = file.readlines()

    lines = [line.strip() for line in data if line.strip()]

    vals = {}
    for line in lines:
        # Split at ':'
        try:
            left, right = line.split(':')
        except ValueError:
            print(f"Skipping malformed line: {line}")
            continue
        key = int(left.strip())
        # Split the right part into numbers
        values = list(map(int, right.strip().split()))
        if key in vals:
            print(f"Warning: Duplicate target {key} found. Overwriting previous entry.")
        vals[key] = np.array(values)

    return vals


def concatenate(a, b):
    """
    Concatenates two integers by their digits.

    Example:
        concatenate(12, 345) -> 12345
    """
    return int(str(a) + str(b))


def can_make_target(target, numbers):
    """
    Determines if the target can be formed using the numbers in the given order
    with operations: addition, multiplication, and concatenation.

    Parameters:
        target (int): The target number to form.
        numbers (np.array): Array of numbers to use.

    Returns:
        bool: True if the target can be formed, False otherwise.
    """
    # If no numbers, can't make target
    if len(numbers) == 0:
        return False

    # If there's only one number, just check equality
    if len(numbers) == 1:
        return numbers[0] == target

    # Start from the first number and proceed in order without rearranging
    return dfs_check(target, numbers[0], numbers, 1)


def dfs_check(target, current_value, numbers, index):
    """
    Recursively checks if the target can be reached by applying operations
    on the numbers in order starting from the current index.

    Parameters:
        target (int): The target number to form.
        current_value (int): The current accumulated value.
        numbers (np.array): Array of numbers to use.
        index (int): The current position in the numbers array.

    Returns:
        bool: True if the target can be formed, False otherwise.
    """
    # If we've used all numbers, check if we reached the target
    if index == len(numbers):
        return current_value == target

    next_num = numbers[index]

    # Try addition
    if dfs_check(target, current_value + next_num, numbers, index + 1):
        return True

    # Try multiplication
    if dfs_check(target, current_value * next_num, numbers, index + 1):
        return True

    # Try concatenation
    concatenated = concatenate(current_value, next_num)
    if dfs_check(target, concatenated, numbers, index + 1):
        return True

    return False


def process_entry(target, values):
    """
    Processes a single dictionary entry to determine if the target can be formed.

    Parameters:
        target (int): The target number.
        values (np.array): Array of numbers to use.

    Returns:
        tuple: (target, bool) indicating if the target is possible.
    """
    result = can_make_target(target, values)
    return target, result


def day07_part2(data_dict):
    """
    Processes each dictionary entry in parallel to determine if targets can be formed.
    Sums all targets that are possible.

    Parameters:
        data_dict (dict): Dictionary with target as key and numbers array as value.

    Returns:
        int: Sum of all possible targets.
    """
    total_sum = 0

    # Use a thread pool with 16 workers
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = {executor.submit(process_entry, target, values): target for target, values in data_dict.items()}

        for future in as_completed(futures):
            target = futures[future]
            try:
                _, result = future.result()
                print(f"Target {target}, numbers {data_dict[target]}: {'Possible' if result else 'Not possible'}")
                if result:
                    total_sum += target
            except Exception as exc:
                print(f"Target {target} generated an exception: {exc}")

    return total_sum


if __name__ == '__main__':
    start_time = time.time()
    data_dict = load_file('in.txt')
    print("Loaded Data Dictionary:")
    for k, v in data_dict.items():
        print(f"{k}: {v}")
    print("---------------------------------------------------")
    total = day07_part2(data_dict)
    print("---------------------------------------------------")
    print(f"Sum of all possible targets: {total}")
    print(f"Execution Time: {time.time() - start_time:.4f} seconds")

    # Sum of all possible targets: 248427118970829
    # Execution Time: 5.4457 seconds
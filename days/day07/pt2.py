import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple


def load_file(file_path: str) -> List[Tuple[int, np.ndarray]]:
    """
    Loads the input file and parses it into a list of tuples.
    Each tuple contains a target number and a NumPy array of subsequent numbers.

    Example:
        Input Line: "190: 10 19"
        Parsed as: [(190, np.array([10, 19]))]
    """
    data_list = []
    with open(file_path, 'r') as file:
        data = file.readlines()

    lines = [line.strip() for line in data if line.strip()]

    for line_number, line in enumerate(lines, start=1):
        # Split at ':'
        try:
            left, right = line.split(':')
        except ValueError:
            print(f"Skipping malformed line {line_number}: {line}")
            continue
        try:
            key = int(left.strip())
        except ValueError:
            print(f"Skipping line {line_number} with invalid target: {left.strip()}")
            continue
        # Split the right part into numbers
        try:
            values = list(map(int, right.strip().split()))
        except ValueError:
            print(f"Skipping line {line_number} with invalid numbers: {right.strip()}")
            continue
        data_list.append((key, np.array(values)))

    return data_list


def concatenate(a: int, b: int) -> int:
    """
    Concatenates two integers by their digits.

    Example:
        concatenate(12, 345) -> 12345
    """
    return int(str(a) + str(b))


def can_make_target(target: int, numbers: np.ndarray) -> bool:
    """
    Determines if the target can be formed using the numbers in the given order
    with operations: addition, multiplication, and concatenation.

    Parameters:
        target (int): The target number to form.
        numbers (np.ndarray): Array of numbers to use.

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


def dfs_check(target: int, current_value: int, numbers: np.ndarray, index: int) -> bool:
    """
    Recursively checks if the target can be reached by applying operations
    on the numbers in order starting from the current index.

    Parameters:
        target (int): The target number to form.
        current_value (int): The current accumulated value.
        numbers (np.ndarray): Array of numbers to use.
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


def process_entry(entry: Tuple[int, np.ndarray]) -> Tuple[int, bool]:
    """
    Processes a single entry to determine if the target can be formed.

    Parameters:
        entry (Tuple[int, np.ndarray]): A tuple containing the target and its numbers.

    Returns:
        Tuple[int, bool]: The target and a boolean indicating if it's possible.
    """
    target, numbers = entry
    result = can_make_target(target, numbers)
    return target, result


def day07_part2(data_list: List[Tuple[int, np.ndarray]]) -> int:
    """
    Processes each entry in parallel to determine if targets can be formed.
    Sums all targets that are possible.

    Parameters:
        data_list (List[Tuple[int, np.ndarray]]): List of tuples with target and numbers.

    Returns:
        int: Sum of all possible targets.
    """
    total_sum = 0

    # Use a thread pool with 16 workers
    with ThreadPoolExecutor(max_workers=16) as executor:
        # Submit all tasks and map futures to their targets
        futures = {executor.submit(process_entry, entry): entry[0] for entry in data_list}

        for future in as_completed(futures):
            target = futures[future]
            try:
                _, result = future.result()
                print(f"Target {target}, numbers {dict_numbers_repr(data_list, target)}: {'Possible' if result else 'Not possible'}")
                if result:
                    total_sum += target
            except Exception as exc:
                print(f"Target {target} generated an exception: {exc}")

    return total_sum


def dict_numbers_repr(data_list: List[Tuple[int, np.ndarray]], target: int) -> List[int]:
    """
    Retrieves the numbers associated with a target for display purposes.

    Parameters:
        data_list (List[Tuple[int, np.ndarray]]): List of tuples with target and numbers.
        target (int): The target number.

    Returns:
        List[int]: The list of numbers associated with the target.
    """
    # Find the first occurrence of the target
    for entry in data_list:
        if entry[0] == target:
            return entry[1].tolist()
    return []


if __name__ == '__main__':
    start_time = time.time()
    data_list = load_file('in.txt')
    print("Loaded Data List:")
    for idx, (k, v) in enumerate(data_list, start=1):
        print(f"{idx}. Target {k}: Numbers {v}")
    print("---------------------------------------------------")
    total = day07_part2(data_list)
    print("---------------------------------------------------")
    print(f"Sum of all possible targets: {total}")
    print(f"Execution Time: {time.time() - start_time:.4f} seconds")

    # Sum of all possible targets: 248427118972289
    # Execution Time: 5.4951 seconds
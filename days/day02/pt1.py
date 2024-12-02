import numpy as np


def load_to_numpy_arrays_from_file(file_path: str):
    """
    Load the file at the given path and convert each line to a NumPy array.
    :param file_path:
    :return:
    """
    with open(file_path, "r") as file:
        # Read lines from the file
        lines = file.readlines()
    # Convert each line to a NumPy array and add to a list
    numpy_arrays = [np.array(list(map(int, line.split()))) for line in lines]
    return numpy_arrays


def is_array_safe(array):
    """Determine if the array is safe based on the criteria."""
    # Calculate differences between consecutive elements
    differences = np.diff(array)

    # Check if differences are all positive (ascending) or all negative (descending)
    is_ascending = np.all(differences > 0)
    is_descending = np.all(differences < 0)

    # Validate that differences are between 1 and 3
    valid_differences = np.all((np.abs(differences) >= 1) & (np.abs(differences) <= 3))

    # Return True if both conditions are met
    return (is_ascending or is_descending) and valid_differences


def count_safe_arrays(file_path: str):
    """Count the number of safe arrays in the file."""
    # Load the NumPy arrays from the file
    numpy_arrays = load_to_numpy_arrays_from_file(file_path)

    # Initialize the counter
    safe_count = 0

    # Check each array
    for array in numpy_arrays:
        if is_array_safe(array):
            safe_count += 1

    return safe_count


def day02_part1(file_path="day02_input.txt"):

    # Load the NumPy arrays from the file
    numpy_arrays = load_to_numpy_arrays_from_file(file_path)

    # for each NumPy array, determine if each value is valid based on the following criteria:
    # array has to be ascending OR descending, ONLY 1 OF THE TWO
    # the maximum difference betwen 2 descending or ascendiung values has to be at most 3 and at minimum 1
    # if an array is safe then add 1 to the counter
    counter = 0

    safe_arrays_count = count_safe_arrays(file_path)
    print(f"Number of safe arrays: {safe_arrays_count}")


if __name__ == "__main__":
    day02_part1()

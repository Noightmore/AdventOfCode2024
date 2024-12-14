import os
import re
from collections import Counter
import numpy as np
from matplotlib import pyplot as plt
import plotly.graph_objs as go
from plotly.offline import plot

def load_file(file_path: str) -> np.ndarray:
    """
    Loads the input file and parses each line to extract complex numbers p and v.

    Parameters:
        file_path (str): Path to the input data file.

    Returns:
        np.ndarray: 2D NumPy array with shape (N, 2) where each row contains p and v as complex numbers.
    """
    data_pairs = []

    # Define the regex pattern
    # Adjust the pattern if your numbers can be floating-point
    pattern = r'p=(?P<p_real>-?\d+),(?P<p_imag>-?\d+)\s+v=(?P<v_real>-?\d+),(?P<v_imag>-?\d+)'
    regex = re.compile(pattern)

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            match = regex.match(line)
            if match:
                try:
                    # Extract and convert to floats
                    p_real = float(match.group('p_real'))
                    p_imag = float(match.group('p_imag'))
                    v_real = float(match.group('v_real'))
                    v_imag = float(match.group('v_imag'))

                    # Create complex numbers
                    p = complex(p_real, p_imag)
                    v = complex(v_real, v_imag)

                    # Append as a row
                    data_pairs.append([p, v])
                except ValueError as ve:
                    print(f"Value conversion error on line {line_number}: {ve}")
            else:
                print(f"Line {line_number} doesn't match the expected format: {line}")

    if not data_pairs:
        print("No valid data pairs found.")
        return np.array([])  # Return empty array if no data

    # Convert list of lists to 2D NumPy array
    data_array = np.array(data_pairs, dtype=complex)
    return data_array


def wrap_around(coord, min_val, max_val):
    """
    Wraps coordinates that exceed the specified bounds using modulo operation.

    Parameters:
        coord (np.ndarray): Array of coordinate values (real or imaginary parts).
        min_val (float): Minimum allowed value.
        max_val (float): Maximum allowed value.

    Returns:
        np.ndarray: Wrapped coordinate values within bounds.
    """
    range_val = max_val - min_val
    wrapped = (coord - min_val) % range_val + min_val
    return wrapped


def plot_complex_pairs(data_array: np.ndarray):
    """
    Plots the p and v complex numbers on the complex plane.

    Parameters:
        data_array (np.ndarray): 2D NumPy array with shape (N, 2).
    """
    p = data_array[:, 0]
    v = data_array[:, 1]

    plt.figure(figsize=(8, 8))
    plt.scatter(p.real, p.imag, color='blue', label='p', marker='o')
    #plt.scatter(v.real, v.imag, color='red', label='v', marker='x')

    plt.title('Complex Numbers p on the Complex Plane')
    plt.xlabel('Real Part')
    plt.ylabel('Imaginary Part')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()



def plot_complex_with_counts_plotly(data_array: np.ndarray, dim_start=0+0j, dim_end=7+11j):
    """
    Plots complex numbers with counts using Plotly for interactivity.

    Parameters:
        data_array (np.ndarray): 2D NumPy array with shape (N, 2) where each row contains p and v as complex numbers.
        dim_start (complex): Starting point defining plot's lower bounds (default: 0+0j).
        dim_end (complex): Ending point defining plot's upper bounds (default: 7+11j).
    """
    # Ensure that data_array is a 2D array with at least one column
    if data_array.ndim != 2 or data_array.shape[1] < 1:
        raise ValueError("data_array must be a 2D NumPy array with at least one column for 'p' values.")

    # Extract p values (assuming 'p' is in the first column)
    p_values = data_array[:, 0]

    # Convert complex numbers to tuples (real, imag) with rounding to handle floating-point precision
    p_tuples = [ (round(p.real, 5), round(p.imag, 5)) for p in p_values ]

    # Count occurrences of each unique p value
    overlap_counter = Counter(p_tuples)

    # If no p values to plot, exit the function
    if not overlap_counter:
        print("No p values to plot.")
        return

    # Extract unique points and their counts
    points = np.array(list(overlap_counter.keys()))
    counts = np.array(list(overlap_counter.values()))

    # Separate real and imaginary parts
    real = points[:, 0]
    imag = points[:, 1]

    # Define marker sizes based on counts (scaling factor can be adjusted)
    marker_sizes = counts * 40  # Adjust scaling factor as needed

    # Create scatter plot using Plotly
    trace = go.Scatter(
        x=real,
        y=imag,
        mode='markers+text',
        marker=dict(
            size=marker_sizes,
            color=counts,  # Color corresponds to counts
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Count'),
            line=dict(width=1, color='DarkSlateGrey')
        ),
        text=counts,  # Display count as text
        textposition='middle center'
    )

    # Define layout with specified dimensions
    layout = go.Layout(
        title='Complex Numbers p with Overlapping Counts',
        xaxis=dict(
            title='Real Part',
            range=[dim_start.real-1, dim_end.real+1],
            zeroline=True
        ),
        yaxis=dict(
            title='Imaginary Part',
            range=[ dim_end.imag+1,dim_start.imag-1],
            zeroline=True
        ),
        hovermode='closest'
    )

    # Create figure and plot
    fig = go.Figure(data=[trace], layout=layout)
    plot(fig)


def main():
    input_file = 'days/day14/test.txt'  # Replace with your input file path

    # print current working directory
    print("Current working directory: ", os.getcwd())


    data_array = load_file(input_file)

    if data_array.size == 0:
        print("No data to process. Exiting.")
        return

    # Display the structured array
    print("Structured 2D NumPy Array (p and v as complex numbers):")
    print(data_array)

    # test dimension size
    dim_start, dim_end = 0 + 0j, 7 + 11j
    second_count = 100

    plot_complex_with_counts_plotly(data_array, dim_start, dim_end)

    for _ in range(second_count):

        # we need to check if a new position is within the dimension,
        # if not then the new position is going to on the other side of the dimension
        # moved by the remaining steps specified by the velocity


        # move all the robots
        data_array[:, 0] += data_array[:, 1]

        for i in range(data_array.shape[0]):
            data_array[i, 0] = wrap_around(data_array[i, 0].real, dim_start.real, dim_end.real) + wrap_around(data_array[i, 0].imag, dim_start.imag, dim_end.imag) * 1j

    plot_complex_with_counts_plotly(data_array, dim_start, dim_end)
    print(data_array)


if __name__ == "__main__":
    main()

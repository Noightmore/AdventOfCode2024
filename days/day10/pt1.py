import numpy as np
from typing import List, Tuple

def load_grid(file_path: str) -> np.ndarray:
    """
    Loads grid data from a text file into a 2D NumPy array.

    Parameters:
        file_path (str): Path to the input text file.

    Returns:
        np.ndarray: 2D array representing the grid.
    """
    grid = []
    try:
        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    print(f"Skipping empty line {line_number}.")
                    continue  # Skip empty lines
                try:
                    row = [int(char) for char in line]
                except ValueError as e:
                    print(f"Invalid character in line {line_number}: {e}")
                    continue  # Skip lines with non-digit characters
                grid.append(row)
        if not grid:
            print("No valid grid data found in the file.")
        return np.array(grid)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return np.array([])
    except Exception as e:
        print(f"An error occurred while loading the grid: {e}")
        return np.array([])

def find_start_end_positions(grid: np.ndarray) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    """
    Identifies all start (0) and end (9) positions in the grid.

    Parameters:
        grid (np.ndarray): 2D array representing the grid.

    Returns:
        Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
            A tuple containing two lists:
                - List of (row, column) tuples for start positions.
                - List of (row, column) tuples for end positions.
    """
    start_positions = list(zip(*np.where(grid == 0)))
    end_positions = list(zip(*np.where(grid == 9)))
    return start_positions, end_positions

def find_all_trails(grid: np.ndarray) -> int:
    """
    Finds all valid trails from every 0 to 9 in the grid.

    Parameters:
        grid (np.ndarray): 2D array representing the grid.

    Returns:
        int: Total sum of scores of all trailheads.
    """
    ROWS, COLS = grid.shape
    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    # Identify all start (0) and end (9) positions
    start_positions, end_positions = find_start_end_positions(grid)

    print(f"Start positions (0): {start_positions}")
    print(f"End positions (9): {end_positions}\n")

    total_trailhead_scores = 0

    for idx, (x, y) in enumerate(start_positions, start=1):
        reachable_nines = set()
        visited = set()
        visited.add((x, y))
        dfs(grid, x, y, grid[x][y], visited, reachable_nines, ROWS, COLS, DIRECTIONS)
        score = len(reachable_nines)
        print(f"Start {idx}: Position ({x}, {y}) with {grid[x][y]} → {score} trail(s)")
        total_trailhead_scores += score

    return total_trailhead_scores

def dfs(grid: np.ndarray, x: int, y: int, current_num: int, visited: set, reachable_nines: set, ROWS: int, COLS: int, DIRECTIONS: List[Tuple[int, int]]):
    """
    Performs DFS to collect reachable 9's from the current position.

    Parameters:
        grid (np.ndarray): The grid.
        x (int): Current row.
        y (int): Current column.
        current_num (int): Current number on the grid.
        visited (set): Set of visited positions.
        reachable_nines (set): Set to collect reachable 9's.
        ROWS (int): Number of rows in the grid.
        COLS (int): Number of columns in the grid.
        DIRECTIONS (List[Tuple[int, int]]): List of movement directions.
    """
    if current_num == 9:
        reachable_nines.add((x, y))
        return

    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        # Check boundaries
        if 0 <= nx < ROWS and 0 <= ny < COLS:
            if grid[nx][ny] == current_num + 1 and (nx, ny) not in visited:
                visited.add((nx, ny))
                dfs(grid, nx, ny, grid[nx][ny], visited, reachable_nines, ROWS, COLS, DIRECTIONS)
                visited.remove((nx, ny))  # Backtrack

def main():
    # Path to your input file
    file_path = 'in.txt'  # Ensure this path is correct and 'in.txt' is in the same directory

    # Load the grid
    grid = load_grid(file_path)

    # Check if grid is empty
    if grid.size == 0:
        print("Grid is empty or could not be loaded. Please check the input file.")
        return

    print("Loaded Grid:")
    print(grid)
    print("---------------------------------------------------")

    # Find all valid trails
    total_trails = find_all_trails(grid)
    print("---------------------------------------------------")
    print(f"Sum of all trailhead scores: {total_trails}")

if __name__ == "__main__":
    main()

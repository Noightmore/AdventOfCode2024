import re
from functools import cache
from typing import List, Dict



def load_machines(file_path: str) -> List[Dict]:
    """
    Loads the claw machine configurations and prize locations from a data file.

    Each machine is described by three lines:
        Button A: X+<value>, Y+<value>
        Button B: X+<value>, Y+<value>
        Prize: X=<value>, Y=<value>

    Parameters:
        file_path (str): The path to the input data file.

    Returns:
        List[Dict]: A list of dictionaries, each representing a machine.
    """
    machines = []
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]  # Remove empty lines

    # Process lines in chunks of 3
    if len(lines) % 3 != 0:
        print("Warning: The number of lines in the file is not a multiple of 3. Some machines may be incomplete.")

    for i in range(0, len(lines), 3):
        try:
            # Extract Button A data
            button_a_line = lines[i]
            button_a_match = re.match(r'Button A:\s*X\+(\d+),\s*Y\+(\d+)', button_a_line, re.IGNORECASE)
            if not button_a_match:
                raise ValueError(f"Invalid format for Button A on line {i+1}: '{button_a_line}'")
            button_a_x = int(button_a_match.group(1))
            button_a_y = int(button_a_match.group(2))
            button_a_cost = 3  # As per problem statement

            # Extract Button B data
            button_b_line = lines[i+1]
            button_b_match = re.match(r'Button B:\s*X\+(\d+),\s*Y\+(\d+)', button_b_line, re.IGNORECASE)
            if not button_b_match:
                raise ValueError(f"Invalid format for Button B on line {i+2}: '{button_b_line}'")
            button_b_x = int(button_b_match.group(1))
            button_b_y = int(button_b_match.group(2))
            button_b_cost = 1  # As per problem statement

            # Extract Prize data
            prize_line = lines[i+2]
            prize_match = re.match(r'Prize:\s*X=(\d+),\s*Y=(\d+)', prize_line, re.IGNORECASE)
            if not prize_match:
                raise ValueError(f"Invalid format for Prize on line {i+3}: '{prize_line}'")
            prize_x = int(prize_match.group(1))
            prize_y = int(prize_match.group(2))

            offset = 0

            # Create machine record
            machine = {
                'button_A': {'x': button_a_x, 'y': button_a_y, 'cost': button_a_cost},
                'button_B': {'x': button_b_x, 'y': button_b_y, 'cost': button_b_cost},
                'prize': {'x': prize_x + offset, 'y': prize_y + offset}
            }
            machines.append(machine)
        except IndexError:
            print(f"Warning: Incomplete data for a machine starting at line {i+1}. Skipping this machine.")
            continue
        except ValueError as ve:
            print(f"Error: {ve}. Skipping this machine.")
            continue

    return machines


#@cache
def find_min_tokens(button_A, button_B, prize):
    """
    Determines the minimum number of tokens required to reach the prize location.

    Parameters:
        button_A (dict): {'x': dx_A, 'y': dy_A, 'cost': cost_A}
        button_B (dict): {'x': dx_B, 'y': dy_B, 'cost': cost_B}
        prize (dict): {'x': Px, 'y': Py}

    Returns:
        int: Minimum tokens required, or -1 if impossible.
    """
    dx_A, dy_A, cost_A = button_A['x'], button_A['y'], button_A['cost']
    dx_B, dy_B, cost_B = button_B['x'], button_B['y'], button_B['cost']
    Px, Py = prize['x'], prize['y']

    min_tokens = float('inf')
    found = False

    # Maximum possible presses for Button A
    max_a = Px // dx_A if dx_A != 0 else 0

    for a in range(max_a + 1):
        # Remaining X after pressing A
        remaining_x = Px - a * dx_A

        if dx_B == 0:
            if remaining_x != 0:
                continue
            b = 0
        else:
            if remaining_x % dx_B != 0:
                continue
            b = remaining_x // dx_B

        if b < 0:
            continue

        # Check Y-axis
        y_total = a * dy_A + b * dy_B
        if y_total != Py:
            continue

        # Calculate total tokens
        total_tokens = a * cost_A + b * cost_B
        if total_tokens < min_tokens:
            min_tokens = total_tokens
            found = True

    return min_tokens if found else -1

if __name__ == '__main__':
    t = 0
    for machine in load_machines('test.txt'):
        button_A = machine['button_A']
        button_B = machine['button_B']
        prize = machine['prize']
        min_tokens = find_min_tokens(button_A, button_B, prize)
        if min_tokens != -1:
            print(f"Minimum tokens required: {min_tokens}")
            t += min_tokens
        else:
            print("It's impossible to reach the prize with the given button configurations.")

    print(f"Total tokens: {t}")
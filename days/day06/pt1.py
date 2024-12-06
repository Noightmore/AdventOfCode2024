from typing import NoReturn, Tuple, List, Any


#
def load_file(file_path: str) -> list:
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # remove the newline character
        lines = [line.strip() for line in lines]

        return lines


def convert_char_to_complex_orientation(char: str) -> complex:
    if char == "<":
        return -1
    elif char == ">":
        return 1
    elif char == "v":
        return 1j
    elif char == "^":
        return -1j


def record_obstacles(lines: list) -> tuple[list[complex], complex, complex, str | Any]:
    obstacles = []
    box_bounds = len(lines[0]) + len(lines)*1j - (1 + 1j)  # to keep track of the maximum right and bottom bounds

    coords = 0 + 0j
    guard_pos = 0 + 0j
    guard_momentum = ""

    for row in lines:
        for col in row:
            if col == '#':
                obstacles.append(coords)
            elif col in ("<", ">", "v", "^"):
                guard_pos = coords
                guard_momentum = convert_char_to_complex_orientation(col)
            coords += 1

        coords += 1j
        coords -= coords.real

    return obstacles, guard_pos, box_bounds, guard_momentum


def day06_pt1(file_path: str) -> NoReturn:
    lines = load_file(file_path)
    obstacles, guard_pos, box_bounds, guard_momentum = record_obstacles(lines)

    print(f"Obstacles: {obstacles}")
    print(f"Guard Position: {guard_pos}")
    print(f"Box Bounds: {box_bounds}")
    print(f"Guard Momentum: {guard_momentum}")

    print("---------------------------------------------------")

    total_unique_visits = set()
    total_unique_visits |= {guard_pos}

    while box_bounds.real >= guard_pos.real >= 0 and box_bounds.imag >= guard_pos.imag >= 0:
        # we have to check if the next position is not an obstacle then guard moves there and we record the visit
        if guard_pos + guard_momentum not in obstacles:
            guard_pos += guard_momentum
            total_unique_visits |= {guard_pos}

        # if it is an obstacle then we change the direction of the guard to the right by 90 degrees
        else:
            guard_momentum *= 1j

        # visualize the guard's movement
        print(guard_pos)

    print(len(total_unique_visits)-1)


if __name__ == "__main__":
    file_path = "in.txt"
    day06_pt1(file_path)

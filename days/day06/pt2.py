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

    og_guard_pos = guard_pos
    og_guard_momentum = guard_momentum

    while box_bounds.real >= guard_pos.real >= 0 and box_bounds.imag >= guard_pos.imag >= 0:
        # we have to check if the next position is not an obstacle then guard moves there and we record the visit
        if guard_pos + guard_momentum not in obstacles:
            guard_pos += guard_momentum
            total_unique_visits |= {guard_pos}

        # if it is an obstacle then we change the direction of the guard to the right by 90 degrees
        else:
            guard_momentum *= 1j

        # visualize the guard's movement
        #print(guard_pos)

    # The guard stopped when leaving the bounds, remove that last out-of-bounds position if present
    # (Check if guard_pos is still within bounds before removing)
    if not (0 <= guard_pos.real <= box_bounds.real and 0 <= guard_pos.imag <= box_bounds.imag):
        if guard_pos in total_unique_visits:
            total_unique_visits.remove(guard_pos)
    print(len(total_unique_visits))

    total_working_obstacles = 0
    # now given the possible guard path and its starting position, for each new attempt we place a new obstacle at 1
    # of the total unique visits position and see if guard wanders off or returns back to the starting position

    # create a set of all unique positions excluding the starting position and already existing obstacles

    max_horizontal = int(box_bounds.real) + 1
    max_vertical = int(box_bounds.imag) + 1

    # all_positions = set()
    # for row in range(0, max_horizontal):
    #     for col in range(0, max_vertical):
    #         all_positions |= {col + row*1j}
    #
    # positions_to_try = all_positions - {og_guard_pos} - set(obstacles)
    #
    # # convert the set to a list for indexing
    # positions_to_try = list(positions_to_try)

    # We now consider placing a new obstacle
    deltas = [1, -1, 1j, -1j]

    neighbors_of_visits = set()
    for pos in total_unique_visits:
        for d in deltas:
            neighbors_of_visits.add(pos + d)

    # Candidate positions:
    # - Must not be guard's starting pos
    # - Must not be existing obstacles
    # - Must be within the bounding box
    # - Based on total_unique_visits and their neighbors
    positions_to_try = (total_unique_visits | neighbors_of_visits) - {og_guard_pos} - set(obstacles)
    positions_to_try = {p for p in positions_to_try
                        if 0 <= p.real <= box_bounds.real and 0 <= p.imag <= box_bounds.imag}

    positions_to_try = list(positions_to_try)

    print(f"Positions to try: {len(positions_to_try)}")
    bruhs = [238]

    for attempt in range(0, len(positions_to_try)):
        print(f"Attempt: {attempt}")
        print(total_working_obstacles)

        #if attempt in bruhs:
        #    continue

        guard_pos = og_guard_pos
        guard_momentum = og_guard_momentum
        touched_new_obstacle_max_count = 10
        touches_of_new_obstacle = 0

        cycles = 0
        while box_bounds.real >= guard_pos.real >= 0 and box_bounds.imag >= guard_pos.imag >= 0:

            # we have to check if the next position is not an obstacle then guard moves there, and we record the visit
            if guard_pos + guard_momentum not in obstacles and guard_pos + guard_momentum != positions_to_try[attempt]:
                guard_pos += guard_momentum

            # to check if he's in a loop we periodically run into the new obstacle, last in the elements
            elif guard_pos + guard_momentum == positions_to_try[attempt]:
                if touches_of_new_obstacle >= touched_new_obstacle_max_count:
                    total_working_obstacles += 1
                    break
                else:
                    touches_of_new_obstacle += 1
                guard_momentum *= 1j  # do not forget to turn lol

            # if it is an old obstacle then we change the direction of the guard to the right by 90 degrees
            else:
                guard_momentum *= 1j
            cycles += 1

            if cycles > 30000:
                total_working_obstacles += 1
                break
        print(cycles)
    print(total_working_obstacles)


if __name__ == "__main__":
    file_path = "in.txt"
    day06_pt1(file_path)

from typing import NoReturn
import numpy as np
from concurrent.futures import ThreadPoolExecutor


def load_file(file_path: str):
    with open(file_path) as f:
        return [line.rstrip('\n') for line in f]


def record_obstacles(lines):
    obstacles = []
    guard_pos = None
    guard_momentum = None

    direction_map = {
        '>': 1,
        '<': -1,
        'v': 1j,
        '^': -1j
    }

    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == '#':
                obstacles.append(c + r*1j)
            elif char in direction_map:
                guard_pos = c + r*1j
                guard_momentum = direction_map[char]

    box_bounds = (len(lines[0]) - 1) + (len(lines) - 1)*1j
    return obstacles, guard_pos, box_bounds, guard_momentum


def check_attempt(attempt_index, positions_to_try, obstacles, og_guard_pos, og_guard_momentum, box_bounds):
    guard_pos = og_guard_pos
    guard_momentum = og_guard_momentum

    cycles = 0
    max_cycles = 30000  # threshold for considering a loop

    # Attempt to see if placing the obstacle at positions_to_try[attempt_index] leads to a loop
    # Note: We do not modify `obstacles` here, only read from it.
    # The new obstacle is conceptually at positions_to_try[attempt_index], we treat it as blocked.
    new_obstacle = positions_to_try[attempt_index]

    while 0 <= guard_pos.real <= box_bounds.real and 0 <= guard_pos.imag <= box_bounds.imag:
        next_pos = guard_pos + guard_momentum

        if next_pos not in obstacles and next_pos != new_obstacle:
            # Move forward
            guard_pos = next_pos
        elif next_pos == new_obstacle:
            # Hitting the new obstacle means turn right (90 degrees)
            guard_momentum *= 1j
        else:
            # Hit an old obstacle
            guard_momentum *= 1j

        cycles += 1
        if cycles > max_cycles:
            # Consider this a "working" obstacle scenario
            return 1

    # If guard exits the bounds without looping
    return 0


def day06_pt2(file_path: str):
    lines = load_file(file_path)
    obstacles, guard_pos, box_bounds, guard_momentum = record_obstacles(lines)

    print(f"Obstacles: {obstacles}")
    print(f"Guard Position: {guard_pos}")
    print(f"Box Bounds: {box_bounds}")
    print(f"Guard Momentum: {guard_momentum}")

    print("---------------------------------------------------")

    total_unique_visits = {guard_pos}
    og_guard_pos = guard_pos
    og_guard_momentum = guard_momentum

    # Simulate initial route
    while 0 <= guard_pos.real <= box_bounds.real and 0 <= guard_pos.imag <= box_bounds.imag:
        next_pos = guard_pos + guard_momentum
        if next_pos not in obstacles:
            guard_pos = next_pos
            total_unique_visits.add(guard_pos)
        else:
            guard_momentum *= 1j

    # If guard ended out-of-bounds, remove last position
    if not (0 <= guard_pos.real <= box_bounds.real and 0 <= guard_pos.imag <= box_bounds.imag):
        if guard_pos in total_unique_visits:
            total_unique_visits.remove(guard_pos)

    print(len(total_unique_visits))

    # Positions to try: visited positions (except start), excluding existing obstacles
    positions_to_try = list(total_unique_visits - {og_guard_pos} - set(obstacles))

    print(f"Positions to try: {len(positions_to_try)}")

    # Run attempts in parallel
    max_workers = 10  # adjust this based on your machine
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(
            lambda i: check_attempt(i, positions_to_try, obstacles, og_guard_pos, og_guard_momentum, box_bounds),
            range(len(positions_to_try))
        )

    total_working_obstacles = sum(results)
    print(total_working_obstacles)
    return total_working_obstacles


if __name__ == "__main__":
    file_path = "in.txt"
    import time
    start = time.time()
    day06_pt2(file_path)  # 1984
    print(f"Time: {time.time() - start}")


    # 5404
    # Positions to try: 5403
    # 1984
    # Time: 1163.249984741211
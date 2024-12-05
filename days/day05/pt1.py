import re

import numpy as np


def parse_input(input_file):
    with open(input_file, 'r') as file:
        data = file.readlines()

        # remove the newline character from the end of each line
        data = [line.strip() for line in data]

        # while there's not a blank line convert these numbers 34|53 into a dict entry {34: 53}

        pattern = re.compile(r'^(\d+)\|(\d+)$')
        rules = {}
        entries = []

        for line in data:
            line = line.strip()
            if line == '':
                # Skip blank lines
                continue

            match = pattern.match(line)
            if match:
                # Line matches the pattern x|y
                x_val = match.group(1)
                y_val = match.group(2)
                if y_val not in rules:
                    rules[y_val] = []
                rules[y_val].append(x_val)
            else:
                # Line doesn't match the pattern and is not blank
                # Treat as comma-separated integers
                str_values = line.split(',')
                #print(str_values)
                int_values = list(map(int, str_values))
                arr = np.array(int_values)
                entries.append(arr)

        return rules, entries


def day05_part1(input_file='test.txt'):
    rules, entries = parse_input(input_file)
    print(rules)
    print(entries)

    t = 0  # total sum of middle elements for rows that meet all rules

    for i, row in enumerate(entries):
        print(f"Checking row {i}: {row}")
        str_row = list(map(str, row))

        # Flag to indicate if this row meets all rules
        all_rules_met = True

        for y_val, x_list in rules.items():
            if y_val in str_row:
                y_index = str_row.index(y_val)
                # Now we check if all X in rules[Y] appear somewhere before Y
                for x_val in x_list:
                    # Check if x_val is in the portion before y_val
                    if x_val not in str_row[:y_index]:
                        all_rules_met = False
                        break
                if not all_rules_met:
                    break

        if all_rules_met:
            # If all rules are met for this row, add the middle element to t
            mid_index = len(row) // 2
            middle_element = row[mid_index]
            t += middle_element

    print("Total:", t)


if __name__ == "__main__":
    day05_part1()




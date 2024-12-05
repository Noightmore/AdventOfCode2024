import re
import numpy as np


def read_file(filename):
    """
    Reads the file and separates rules and updates.
    Assumes the file has a blank line separating the rules from the updates.
    """
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip() != '']

    # Now 'lines' contains no empty lines, we assume that rules come first until no more match 'X|Y' pattern
    # If you know there's a guaranteed blank line in the file, you can split on that,
    # but here we assume after rules we have updates directly.

    # A safer approach is:
    pattern = re.compile(r'^\d+\|\d+$')

    # Separate rules from updates:
    rules_lines = []
    updates_lines = []
    mode = 'rules'
    for line in lines:
        if mode == 'rules':
            # If it's still matching the rule pattern, it's a rule
            if pattern.match(line):
                rules_lines.append(line)
            else:
                # Once we hit a line that doesn't match a rule, treat it as an update line
                mode = 'updates'
                updates_lines.append(line)
        else:
            updates_lines.append(line)

    return rules_lines, updates_lines


def parse_rules(rule_lines):
    pattern = re.compile(r'^(\d+)\|(\d+)$')
    rules = []
    for line in rule_lines:
        match = pattern.match(line)
        if match:
            x_val = int(match.group(1))
            y_val = int(match.group(2))
            rules.append((x_val, y_val))
    return rules


def parse_updates(update_lines):
    updates = []
    for line in update_lines:
        str_values = line.split(',')
        int_values = list(map(int, str_values))
        arr = np.array(int_values)
        updates.append(arr)
    return updates


def update_is_correct(update, rules):
    update_list = update.tolist()
    for (X, Y) in rules:
        if X in update_list and Y in update_list:
            x_index = update_list.index(X)
            y_index = update_list.index(Y)
            if x_index > y_index:  # X must come before Y
                return False
    return True


def sum_middle_of_correct_updates(rule_lines, update_lines):
    rules = parse_rules(rule_lines)
    updates = parse_updates(update_lines)

    total = 0
    for update in updates:
        if update_is_correct(update, rules):
            mid_index = len(update) // 2
            total += update[mid_index]
    return total


if __name__ == "__main__":
    # Replace 'input.txt' with the actual filename
    rule_lines, update_lines = read_file('in.txt')

    rules = parse_rules(rule_lines)
    updates = parse_updates(update_lines)

    #print("Rules:", rule_lines)
    #print("Updates:", update_lines)
    #print("Parsed rules:", rules)
    #print("Parsed updates:", updates)

    result = sum_middle_of_correct_updates(rule_lines, update_lines)
    print("Total:", result)

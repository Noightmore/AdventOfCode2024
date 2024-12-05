import re
import numpy as np
from collections import defaultdict, deque


def read_file(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip() != '']

    pattern = re.compile(r'^\d+\|\d+$')
    rules_lines = []
    updates_lines = []
    mode = 'rules'

    for line in lines:
        if mode == 'rules':
            # Check if it's a rule
            if pattern.match(line):
                rules_lines.append(line)
            else:
                # Now we switch to updates
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


def topological_sort(nodes, edges):
    """
    Perform a topological sort on the given graph.
    nodes: set or list of nodes
    edges: dict mapping node -> list of nodes it points to
    Returns a list representing one valid topological ordering of nodes.
    """
    # Compute in-degrees
    in_degree = {n:0 for n in nodes}
    for n in edges:
        for nxt in edges[n]:
            in_degree[nxt] += 1

    # Queue for nodes with in-degree 0
    queue = deque([n for n in nodes if in_degree[n] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in edges[node]:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)

    # If order doesn't include all nodes, there's a cycle or issue.
    if len(order) != len(nodes):
        # This would mean a cycle in the rules, which should not happen.
        # But in case it does, we return what we have.
        pass
    return order


def reorder_update(update, rules):
    """
    Reorder the given update according to the rules.
    Steps:
    - Identify pages in the update.
    - Extract applicable rules (both pages in the update).
    - Create a directed graph representing these rules.
    - Perform a topological sort to find a valid order.
    - The topological sort gives an order for pages that appear in rules.
      If some pages are not in any rule, they still appear as isolated nodes.
    """
    update_list = update.tolist()
    update_set = set(update_list)

    # Build graph from applicable rules
    edges = defaultdict(list)
    nodes = set(update_list)  # all pages in the update are nodes
    for (X, Y) in rules:
        if X in update_set and Y in update_set:
            # X must come before Y
            edges[X].append(Y)

    # Ensure every node is in edges dict
    for n in nodes:
        if n not in edges:
            edges[n] = []

    sorted_pages = topological_sort(nodes, edges)

    # 'sorted_pages' now represents a valid ordering that satisfies the rules.
    # One subtlety: topological sort will produce a valid order among constrained nodes.
    # Unconstrained pages (no edges) will appear as they are.
    # Because we included all pages in nodes, they should appear in sorted_pages.

    return np.array(sorted_pages)


def sum_middle_of_reordered_incorrect_updates(rule_lines, update_lines):
    rules = parse_rules(rule_lines)
    updates = parse_updates(update_lines)

    total = 0
    for update in updates:
        if not update_is_correct(update, rules):
            correct_update = reorder_update(update, rules)
            mid_index = len(correct_update) // 2
            total += correct_update[mid_index]
    return total


if __name__ == "__main__":
    # Example usage (using the example from Part Two):
    rule_lines, update_lines = read_file('in.txt')

    # Sum of middle pages after reordering just the incorrectly-ordered updates
    part_two_total = sum_middle_of_reordered_incorrect_updates(rule_lines, update_lines)
    print("Part Two Total:", part_two_total)

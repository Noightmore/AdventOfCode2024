def read_input(file='test.txt'):
    needed_combinations = []
    with open(file, 'r') as f:
        avaible_towels = f.readline().strip().split(', ')

        _ = f.readline()

        for line in f:
            needed_combinations.append(line.strip())

    return avaible_towels, needed_combinations


def can_be_arranged(towels, c):
    cursor = 0
    while cursor < len(c):
       # check if any word from towels is a substring in c a starting at cursor
        longest_match = 0
        for t in towels:
            if c[cursor:].startswith(t):
                if len(t) > longest_match:
                    longest_match = len(t)
                continue

            if t == towels[-1] and longest_match == 0:
                return False
        cursor += longest_match
    return True


def dfs_combinations(towels, comb):
    for c in comb:
        yield can_be_arranged(towels, c)



def day19_pt1():
    towels, comb = read_input('test.txt')
    print(towels)
    print(comb)

    possible_towels = dfs_combinations(towels, comb)
    #print(list(possible_towels))

    # get count of trues
    print(sum(possible_towels))

    # only take towels that have true next to them

if __name__ == '__main__':
    day19_pt1()

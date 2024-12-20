from functools import lru_cache


def read_input(file='test.txt'):
    needed_combinations = []
    with open(file, 'r') as f:
        avaible_towels = f.readline().strip().split(', ')

        _ = f.readline()

        for line in f:
            needed_combinations.append(line.strip())

    return tuple(avaible_towels), needed_combinations


@lru_cache(maxsize=None)
def can_be_arranged(towels, c):

    for i in range(0,len(c)):
       # check if any word from towels is a substring in c a starting at cursor
        for t in towels:
            if c[i:] == t:
                return True
            if c[i:].startswith(t):
                #print(f"matched {t} in {c[i:]}")
                match = can_be_arranged(towels, c[len(t):])
                if match:
                    return True

        return False


def dfs_combinations(towels, comb):

    for c in comb:
        yield can_be_arranged(towels, c)



def day19_pt1():
    towels, comb = read_input('in.txt')
    print(towels)
    print(comb)

    possible_towels = dfs_combinations(towels, comb)
    print(sum(possible_towels))
    #print(list(possible_towels))

    # get count of trues


    # only take towels that have true next to them

def debug(c):
    towels, comb = read_input('test.txt')
    print(towels, c)
    print(can_be_arranged(towels, c))

if __name__ == '__main__':
    day19_pt1()
    #debug('bwurrg')

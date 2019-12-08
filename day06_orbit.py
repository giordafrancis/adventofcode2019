
import re
from typing import NamedTuple, List, Dict

class Orbit(NamedTuple):
    parent: str
    child: str

    @staticmethod #very cool
    def parse_string(input:str)-> 'Orbit':
        parent, child = input.strip().split(')')
        return Orbit(parent, child)

TEST_INPUT = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""

def make_orbits(inputs: str) -> List[Orbit]:
    return [Orbit.parse_string(s) for s in inputs.split('\n')]

def make_tree(orbits: List[Orbit]) -> Dict[str, str]:
    parents = {}
    for parent, child in orbits:
        parents[child] = parent
    return parents

PARENTS = make_tree(make_orbits(TEST_INPUT))

def count_ancestors(child: str, parents: Dict[str, str]) -> int:
    count = 0
    while child != "COM":
        #print("child->", child, "count->", count)
        count += 1
        child = parents[child]
    #print("final count->", count)
    return count

assert count_ancestors('D', PARENTS) == 3
assert count_ancestors('L', PARENTS) == 7
assert count_ancestors('COM', PARENTS) == 0

def total_orbits(parents: Dict[str,str]) -> int:
    return sum(count_ancestors(child, PARENTS) for child in parents)

assert total_orbits(PARENTS) == 42

# PART 2
TEST_INPUT2 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""

PARENTS = make_tree(make_orbits(TEST_INPUT2))

def find_path(child: str, parents: Dict[str, str]) -> Dict[str,str]:
    path = {}
    while child != "COM":
        path[child] = parents[child]
        child = parents[child]
    return path

def find_common_parent(parents: Dict[str, str], start:str = 'YOU', end:str='SAN') -> str:
    path1= reversed(list(find_path(start, parents))) # from COM
    path2 = reversed(list(find_path(end, PARENTS)))
    for child1,child2 in zip(path1, path2):
        if child1 == child2:
            last_common = child1
        else:
            return last_common

def min_transfers(parents: Dict[str, str], start:str = 'YOU', end:str='SAN'):
    commom_parent = find_common_parent(parents,start,end)
    print(commom_parent)
    min_travel = 0
    for child in (start, end):
        #print(f'checking child {child}')
        child = parents[child]
        while child != commom_parent:
            child = parents[child]
            min_travel += 1
            #print('now child is', child, 'distance_traveled so far', min_travel)
    return min_travel

assert min_transfers(PARENTS) == 4
assert min_transfers(PARENTS, start='H', end='SAN') == 4
assert min_transfers(PARENTS, start='L', end='F') == 2


if __name__ == "__main__":
    with open('day06_input.txt', 'r') as file:
        ORBITS = make_orbits(inputs=file.read())
        PARENTS = make_tree(orbits=ORBITS)
        print('total orbits part1->',total_orbits(parents=PARENTS))
        print('min orbital transfer is part2->',min_transfers(parents=PARENTS))

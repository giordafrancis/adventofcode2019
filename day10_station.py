"""
https://adventofcode.com/2019/day/10
"""

from typing import List, NamedTuple, Iterator, Tuple, Dict
from collections import defaultdict
import math

class Asteroid(NamedTuple):
    x: int
    y: int

Asteroids = List[Asteroid]

def parse_raw(inputs:str)->Iterator[str]:
    for row in inputs.strip().split("\n"):
        yield row

def to_asteroids(inputs:str) -> Asteroids:
    inputs = parse_raw(inputs)
    return [Asteroid(x,y)
            for y, row in enumerate(inputs)
                for x, char in enumerate(row)
                    if char == "#"
            ]

def detect_asteroids(asteroids: Asteroids, station: Asteroid) -> Tuple[int, Asteroid]:

    slopes= set()
    for x, y  in asteroids:
        dx = x - station.x
        dy = y - station.y
        
        gcd = math.gcd(dy, dx)

        if dy == dx == 0: #station = asteroid
            continue
        # print(dy,dx,gcd)
        # print((dy / gcd, dx / gcd))
        slopes.add((dy / gcd, dx / gcd))
    # print(slopes)
    return len(slopes), station

def compare_stations(asteroids: Asteroids) -> int:
    return max(detect_asteroids(asteroids, station)  
                for station in asteroids
                )

TEST1=""".#..#
.....
#####
....#
...##"""


# asteroids = to_asteroids(TEST1)
# station = Asteroid(3,4)
# print(detect_asteroids(asteroids, station))
# print(compare_stations(asteroids))


asteroids = to_asteroids("""#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""")

#print(compare_stations(asteroids))

asteroids = to_asteroids(""".#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..""")

#print(compare_stations(asteroids))

asteroids = to_asteroids(""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""")

#print(compare_stations(asteroids))

PUZZLE = to_asteroids(""".###..#######..####..##...#
########.#.###...###.#....#
###..#...#######...#..####.
.##.#.....#....##.#.#.....#
###.#######.###..##......#.
#..###..###.##.#.#####....#
#.##..###....#####...##.##.
####.##..#...#####.#..###.#
#..#....####.####.###.#.###
#..#..#....###...#####..#..
##...####.######....#.####.
####.##...###.####..##....#
#.#..#.###.#.##.####..#...#
..##..##....#.#..##..#.#..#
##.##.#..######.#..#..####.
#.....#####.##........#####
###.#.#######..#.#.##..#..#
###...#..#.#..##.##..#####.
.##.#..#...#####.###.##.##.
...#.#.######.#####.#.####.
#..##..###...###.#.#..#.#.#
.#..#.#......#.###...###..#
#.##.#.#..#.#......#..#..##
.##.##.##.#...##.##.##.#..#
#.###.#.#...##..#####.###.#
#.####.#..#.#.##.######.#..
.#.#####.##...#...#.##...#.""")

#print(compare_stations(asteroids))

# Part 2

def clockwise_angle(asteroid):
    """
    ...
    .X.
    ...
    (x,y) clockwise scheme X as the origin. 
    [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    """
    dx, dy = asteroid
    if dx == 0 and dy < 0: # up first
        return (0,0)
    elif dx > 0 and dy < 0:
        # e.g. (0.1, -0.9) or (0.9, -0.1)
        return (1, dx / abs(dy))
    elif dx > 0 and dy == 0:
        return (2, 0)
    elif dx > 0 and dy > 0:
        # e.g. (0.9, 0.1) or (0.1, 0.9)
        return (3, dy / dx)
    elif dx == 0 and dy > 0:
        return (4, 0)
    elif dx < 0 and dy > 0:
        # e.g. (-0.1, 0.9) or (-0.9, 0.1)
        return (5, abs(dx) / dy)
    elif dx < 0 and dy == 0:
        return (6, 0)
    elif dx < 0 and dy < 0:
        # e.g. (-0.9, -0.1) or (-0.1, -0.9)
        return (7, dy / dx)


def asteroids_angle(asteroids: Asteroids, station: Asteroid) -> None:

    asteroids_by_angle: Dict[Tuple[int], List(Asteroid)] = defaultdict(list)
    
    for ast in asteroids:
        dx = ast.x - station.x
        dy = ast.y - station.y
        
        gcd = math.gcd(dx, dy)

        if dy == dx == 0: #station = asteroid
            continue
        angle = (dx / gcd, dy / gcd)
        asteroids_by_angle[angle].append(ast)

    # sort by length to station, closest in last  idx so .pop can be used 
    for angle_asteroids in asteroids_by_angle.values():
        angle_asteroids.sort(key = lambda a: abs(a.x - station.x) 
                                    + abs(a.y - station.y), 
                        reverse = True)
    
    while asteroids_by_angle:
        keys = asteroids_by_angle.keys()
        keys =sorted(keys, key=clockwise_angle)

        for key in keys:
            angle_asteroids = asteroids_by_angle[key]
            yield angle_asteroids.pop()
            if not angle_asteroids:
                del asteroids_by_angle[key]

STATION = Asteroid(8,3)

asteroids = to_asteroids(""".#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##""")

NEW_STATION = compare_stations(PUZZLE)[1]

vaporized1 = list(asteroids_angle(PUZZLE, NEW_STATION))
print(vaporized1[199])



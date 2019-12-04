"""
https://adventofcode.com/2019/day/3
"""

from typing import NamedTuple, List, Pattern, Iterator, Dict, Set
from functools import lru_cache
import re

patt = re.compile("(?P<axis>[L|R|U|D])(?P<distance>[0-9]+)")

class Command(NamedTuple):
    axis: str
    distance: int

class XY(NamedTuple):
    x: int
    y: int

def parse_wire(moves: List[str], pattern: Pattern) -> Iterator[Command]:
    """
    Parse wires commands
    """
    for command in moves:
        g = pattern.search(command)
        yield Command(axis=g.group("axis"),
                      distance=int(g.group('distance')))

def move_wire(moves: List[str], pattern: Pattern) -> Dict[XY, int]:
    """
    Calculates a Dict of XY keys and num_steps as values 
    based on Commands parsing
    """
    commands = parse_wire(moves, pattern)
    locs= {} # all wires start at (0,0)
    x = y = num_steps = 0
    for command in commands:
        axis = command.axis
        distance = command.distance
        for _ in range(distance): # as its inclusive of total distance
            if axis == "R":
                x += 1
            elif axis == "L":
                x -= 1
            elif axis == "U":
                y += 1
            elif axis == "D": 
                y -= 1
            else:
                raise ValueError(f"not a valid axis {axis}")
            num_steps += 1
            locs[XY(x,y)] = num_steps
    return locs

def _parse_string(inputs: str)-> Iterator[Dict[XY,int]]:
    """
    helper function to clean the string input
    into a list of Coordinates
    """
    wires = iter(wire.split(',') for wire in inputs.split("\n"))
    for wire in wires:
        yield move_wire(moves= wire, pattern= patt) # patt hardcoded.           

def manhattan_distance(coord1:XY, coord0:XY=(0,0)) -> int:
    x1, y1 = coord1
    x0, y0 = coord0
    return abs(x1 - x0 ) + abs(y1 - y0)

def crossed_wires(inputs: str) -> int:
    """
    finds intersection and returns closest to origin (0,0)
    """
    wires = _parse_string(inputs)
    wire1, wire2 = set(next(wires)), set(next(wires)) # hardcoded for 2 wires for part 1 & 2
    crossed_at = wire1.intersection(wire2) # on the keys only XY
    return min(manhattan_distance(coords) 
               for coords in crossed_at)

test_string = """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"""
assert crossed_wires(test_string) == 159

test_string = """R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"""
assert crossed_wires(test_string) == 135

test_string = """R8,U5,L5,D3
U7,R6,D4,L4"""
assert crossed_wires(test_string) == 6

# PART2 

def crossed_wires_travel(inputs: str) -> int:
    """
    Returns the min  traveled distance for all 
    wires intersections
    """
    wires = _parse_string(inputs)
    wire1, wire2 = next(wires), next(wires) # hardcoded for 2 wires for part 1 & 2
    crossed_at = set(wire1).intersection(set(wire2))
    return min((wire1[xy] + wire2[xy]) 
                for xy in crossed_at)

test_string = """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"""
assert crossed_wires_travel(test_string) == 610

test_string = """R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"""
assert crossed_wires_travel(test_string) == 410

test_string = """R8,U5,L5,D3
U7,R6,D4,L4"""
assert crossed_wires_travel(test_string) == 30

if __name__ == "__main__":
    with open("day03_input.txt", 'r') as file:
        inputs = file.read()
        part1 = crossed_wires(inputs)
        print("part1 min distance to origin is->", part1)
        part2 = crossed_wires_travel(inputs)
        print("part2 min travel distance is->", part2)































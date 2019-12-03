"""
https://adventofcode.com/2019/day/3
"""

from typing import NamedTuple, List, Pattern, Iterator, Tuple, Dict
from collections import defaultdict
import re

patt = re.compile("(?P<axis>[L|R|U|D])(?P<distance>[0-9]+)")

Coords = Tuple[int]

class Command(NamedTuple):
    axis: str
    distance: int

class Coordinates(NamedTuple):
    wire_name: str
    coords: List[Coords]

def parse_wire(moves: List[str], pattern: Pattern) -> Iterator[Command]:
    """
    Parse wires commands
    """
    for command in moves:
        g = pattern.search(command)
        yield Command(axis=g.group("axis"),
                      distance=int(g.group('distance')))

def move_wire(wire_name:str, moves: List[str], pattern: Pattern) -> Coordinates:
    """
    Calculates list of Coordinates based on Commands
    """
    commands = parse_wire(moves, pattern)
    coords = [(0,0)] # all wires start at (0,0)
    for command in commands:
        x, y = coords[-1]
        axis = command.axis
        distance = command.distance + 1 # its inclusive of total distance
        if axis == "R" or axis == "L": # x case
            if axis == "R":
                for i in range(1, distance): # 0 start will lead to duplicates at joints
                    coords.append((x + i, y)) 
            else:
                for i in range(1, distance):
                    coords.append((x - i, y))
        elif axis == "U" or axis == "D": # y case
            if axis == "U":
                for i in range(1, distance):
                    coords.append((x, y + i))     
            else:
                for i in range(1, distance):
                    coords.append((x, y - i)) 
        else:
            raise ValueError(f"not a valid axis {axis}")

    return Coordinates(wire_name= wire_name,
                       coords = coords)

def _parse_string(inputs: str)-> List[Coordinates]:
    """
    helper function to clean the string input
    into a list of Coordinates
    """
    wires = [wire.split(',') for wire in inputs.split("\n")]
    return [move_wire(wire_name=f"wire_{i}",moves= wire, pattern= patt) # patt hardcoded..
                    for i, wire in zip(range(len(wires)), wires)]

def manhattan_distance(coord1: Coords, coord0:Coords = (0,0)) -> int:
    x1, y1 = coord1
    x0, y0 = coord0
    return abs(x1 - x0 ) + abs(y1 - y0)

def crossed_wires(inputs: str) -> int:
    """
    finds intersection and returns closest to origin (0,0)
    """
    wires = _parse_string(inputs)

    wire1 = set(wires[0].coords) # hardcoded for 2 wires for part 1
    wire2 = set(wires[1].coords)
    crossed_at = wire1.intersection(wire2)
    return min(manhattan_distance(coords) 
               for coords in crossed_at 
               if coords != (0,0))

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
    """
    wires = _parse_string(inputs)
    wire1 = wires[0]
    wire2 = wires[1]
    travel_wire1 = _dict_cords(wire1)
    travel_wire2 = _dict_cords(wire2)
    crossed_at = [coords for coords in wire1.coords if coords in wire2.coords]
    return min((travel_wire1[coords] + travel_wire2[coords]) 
                for coords in crossed_at
                if coords != (0,0))


def _dict_cords(wire: Coordinates) -> Dict[Coords, List]:
    """
    """
    coord_travel = defaultdict(int)
    coord_travel[(0,0)] = 0
    distance = 0 
    for coord0, coord1 in zip(wire.coords, wire.coords[1:]):
        distance += manhattan_distance(coord1, coord0)
        if coord_travel[coord1]:
            continue # if value already, do nothing as we want the first pass
        else:
            coord_travel[coord1] = distance
    return coord_travel

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































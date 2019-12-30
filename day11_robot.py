"""
https://adventofcode.com/2019/day/11
"""

"""
- The intcode is the brains of the robot
- robot will require a grid 
- The program uses input instructions:
    - provide 0 if the robot is over a black panel or 1 if white.
    - the program will output 2 values
        - the color of the panel the robot is over
        - second the direction the robot should turn
            - 0 left 90 degrees
            - 1 right 90 degrees
    - after it turns the robot should move exactly one panel. 
- The robot will continue running for a while like this and halt when it is finished drawing. Do not restart the Intcode computer inside the robot during this process.
"""

from typing import List, NamedTuple, Tuple, Union
from enum import Enum
from collections import deque
import copy

IJ = Tuple[int,int]
Grid = List[List[int]]

class TrackRobot(NamedTuple):
    loc: IJ # (i, j) 
    facing: str #  ('UP','DOWN','LEFT','RIGHT')

class Opcode(Enum): 
    ADD = 1
    MULTIPLY = 2
    STORE_INPUT = 3
    SEND_TO_OUTPUT = 4
    JUMP_IF_TRUE = 5 
    JUMP_IF_FALSE = 6 
    LESS_THAN = 7 
    EQUALS = 8 
    ADJUST_RELATIVE_BASE = 9 
    PROGRAM_HALT = 99

class Modes(NamedTuple):
    opcode: int
    mode1: int
    mode2: int
    mode3: int 

def parse_opcode(input: int) -> Modes:
    padded = f"{input:05}"
    return Modes(opcode= Opcode(int(padded[-2:])), 
                      mode1= int(padded[-3]), 
                      mode2=int(padded[-4]), 
                      mode3=int(padded[-5]))  

def problem_prep(problem_input: str) -> List[int]:
    inputs = [int(num) for num in problem_input.strip().split(",")]
    return inputs

def handle_mode(program: List[int], pos: int, mode: int, relative_base: int)-> int:
        immediate_parameter = program[pos]
        if mode == 0 :
            # position mode
            return program[immediate_parameter]
        elif mode == 1:
            # immediate mode
            return  immediate_parameter
        elif mode == 2:
            # relative mode
            return program[immediate_parameter + relative_base] 
        else:
            raise ValueError(f"unknown mode: {mode} at pos {pos}")

def _loc(program: List[int], pos: int, mode: int, relative_base: int)-> int:
    """
    handles the writting instruction location , either in position or relative mode. 
    We need to know the loc where the value will be written to in the program
    """
    immediate_parameter = program[pos]
    if mode == 0:
        # position mode
        return immediate_parameter
    elif mode == 2:
        # relative mode
        return immediate_parameter + relative_base



def run_intcode(program: List[int], part2: bool = True, offset :int = 20) -> Union[int, Grid]:
    """
    Programs takes an input, 9 + 1 opcodes are valid
    Parameter mode suport is available for 6 opcodes
    pointer(i) is incremented by the number of values in the instruction
    """
    program = program[:]
    initial_loc = (0, 0)
    robot = TrackRobot(loc = initial_loc, facing='UP') # start the robot
    grid = create_grid() # 80 x 80
    grid_loc = {} # track painted locs
    
    if part2:
        row, col = initial_loc
        grid_loc[initial_loc] = 1 # part 2 requirement
        grid[row + offset][col + offset] = 1   # offset of 20 , (0,0) is (20,20) on grid      
    
    for _ in range(10000):
        program.append(0)  # add program large memory, lazy solution

    outputs = deque([])
    pos = relative_base =  0

    while True:
        modes = parse_opcode(program[pos])
        opcode = modes.opcode
        if opcode == Opcode.PROGRAM_HALT: 
            break
        elif opcode == Opcode.ADD:
            num1 = handle_mode(program, pos + 1, modes.mode1, relative_base)
            num2 = handle_mode(program, pos + 2, modes.mode2, relative_base)
            loc = _loc(program, pos + 3, modes.mode3, relative_base)
            program[loc] = num1 + num2        
            pos += 4
        elif opcode == Opcode.MULTIPLY: 
            num1 = handle_mode(program, pos + 1, modes.mode1, relative_base)
            num2 = handle_mode(program, pos + 2, modes.mode2, relative_base)
            loc = _loc(program, pos + 3, modes.mode3, relative_base)
            program[loc] = num1 * num2
            pos += 4
        elif opcode == Opcode.JUMP_IF_TRUE:
            num1 = handle_mode(program, pos + 1, modes.mode1, relative_base)
            num2 = handle_mode(program, pos + 2, modes.mode2, relative_base)
            pos = num2 if num1 else pos + 3
        elif opcode == Opcode.JUMP_IF_FALSE: 
            num1 = handle_mode(program, pos + 1, modes.mode1, relative_base)
            num2 = handle_mode(program, pos + 2, modes.mode2, relative_base) 
            pos = num2 if not num1 else pos + 3
        elif opcode == Opcode.LESS_THAN: 
            num1 = handle_mode(program, pos + 1, modes.mode1, relative_base)
            num2 = handle_mode(program, pos + 2, modes.mode2, relative_base)
            loc = _loc(program, pos + 3, modes.mode3, relative_base)
            program[loc] = 1 if num1 < num2 else 0
            pos += 4
        elif opcode == Opcode.EQUALS: 
            num1 = handle_mode(program, pos + 1, modes.mode1, relative_base)
            num2 = handle_mode(program, pos + 2, modes.mode2, relative_base)
            loc = _loc(program, pos + 3, modes.mode3, relative_base)
            program[loc] = 1 if num1 == num2 else 0
            pos += 4
        elif opcode == Opcode.STORE_INPUT: 
            loc = _loc(program, pos + 1, modes.mode1, relative_base)
            input =  grid_loc.get(robot.loc, 0) # if loc not in grid assumed black
            program[loc] = input
            pos += 2
        elif opcode == Opcode.SEND_TO_OUTPUT:
            output = handle_mode(program, pos + 1, modes.mode1, relative_base)
            outputs.append(output)
            if len(outputs) == 2:
                paint = outputs.popleft() # first instruction
                turn = outputs.popleft()
                grid_loc[robot.loc] = 1 if paint == 1 else 0 # paint the grid_loc[loc] white else paint visited loc black
                if part2:
                    row, col = robot.loc
                    if paint == 1:
                        grid[row + offset][col + offset] = 1 
                    else:
                        grid[row + offset][col + offset] = 0
                now_facing = turn_robot(turn=turn, facing=robot.facing)
                new_loc = move_robot(loc=robot.loc, facing=now_facing)
                robot = TrackRobot(loc=new_loc, facing=now_facing)           
            pos += 2
        elif opcode == Opcode.ADJUST_RELATIVE_BASE:
            num1 = handle_mode(program, pos + 1, modes.mode1, relative_base)
            relative_base += num1
            pos += 2
        else:
            raise RuntimeError(f"invalid opcode {opcode} at position {pos}")
    return grid if part2 else len(grid_loc)

def turn_robot(turn: int, facing: str) -> str:
    """
    Given instruction turn, rotate the robot 
    """
    clockwise = {'UP': 'RIGHT','RIGHT': 'DOWN', 'DOWN': 'LEFT', 
                'LEFT':'UP'}
    counter_clockwise = {'UP': 'LEFT', 'LEFT': 'DOWN', 'DOWN': 'RIGHT',
                        'RIGHT': 'UP'}
    if turn == 1: 
        return clockwise[facing]
    elif turn == 0:
        return counter_clockwise[facing]
    else:
        raise ValueError(f'unknown instruction{turn}')

assert turn_robot(1, 'UP') == 'RIGHT'
assert turn_robot(0, 'UP') == 'LEFT'
assert turn_robot(0, 'DOWN') == 'RIGHT'
assert turn_robot(1,'DOWN') == 'LEFT'
assert turn_robot(0,'LEFT') == 'DOWN'
assert turn_robot(1,'RIGHT') == 'DOWN'
assert turn_robot(1,'LEFT') == 'UP'

def move_robot(loc: IJ, facing: str) -> IJ:
    row, col = loc
    if facing == 'UP':
        row += 1
    elif facing == 'DOWN':
        row -= 1
    elif facing == 'LEFT':
        col -= 1
    elif facing == 'RIGHT':
        col += 1
    else: 
        raise ValueError(f'incorrect value for facing{facing}')
    return row, col

assert move_robot((0, 0), 'UP') == (1,0)
assert move_robot((1, 0), 'LEFT') == (1,-1)
assert move_robot((1,-1), 'DOWN') == (0,-1)
assert move_robot((0,-1), 'RIGHT') == (0,0)
assert move_robot((2,-2), 'LEFT') == (2, -3)
assert move_robot((-3,-4), 'LEFT') == (-3, -5)
assert move_robot((-3,-4), 'RIGHT') == (-3, -3)
assert move_robot((-3,-4), 'UP') == (-2, -4)
assert move_robot((-3,-4), 'DOWN') == (-4, -4)

# PART 2 

def create_grid(rows: int=80, columns: int=80) -> Grid:
    """
    80 x 80 matrix by default 
    eyeballed for registration identifier printing
    set to black (0)"""
    return [[0
        for _ in range(rows)]
        for _ in range(columns)
        ]

def get_image(grid: Grid, columns: int = 80, rows: int = 80)-> List[List[str]]:
    hull = list(reversed(copy.deepcopy(grid))) # image is upside down 
    for i in range(rows):
        for j in range(columns):
            color = hull[i][j]
            if color == 0 :
                hull[i][j] = " "  # easier to read
            else:
                hull[i][j] = "\u2588"
    return hull

def print_image(grid: Grid, columns: int = 80, rows: int = 80)-> str:
    image_hull = get_image(grid, columns, rows)
    image = []
    for row in image_hull:
        image.append("".join(row))
    return "\n".join(image)

if __name__ == "__main__":
    with open('day11_puzzle.txt', 'r') as file:
        program = problem_prep(file.read())
        #print(program, len(program))
        part1 = run_intcode(program=program, part2=False)
        grid = run_intcode(program=program, part2=True)
        print('total unique loc painted', part1)
        print('registration identifier part2',print_image(grid)[4500:5500]) # crop image


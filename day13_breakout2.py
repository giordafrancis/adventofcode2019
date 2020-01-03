"""
https://adventofcode.com/2019/day/13
"""

"""

Second attempt resolved using OOP
- The arcade cabinet runs Intcode software (day09 -> intcode.py)
- It has a primitive screen capable of drawing square tiles on a grid.
- outputs instructions 3 output
    - outputs 0 -> distance to the left 
    - outputs 1 -> distance to the right
    - outputs 3 tile id (enum):
        -> 0 empty .... 4 ball tile
"""

from typing import NamedTuple, Optional, DefaultDict, List, Dict, Set
from enum import Enum
from collections import deque, defaultdict
import copy

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

class TilesID(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

class XY(NamedTuple):
    x: int
    y: int

class Modes(NamedTuple):
    opcode: int
    mode1: int
    mode2: int
    mode3: int 

class EndProgram(Exception): pass

Tiles_Loc = Dict[XY, TilesID]

def parse_opcode(input: int) -> Modes:
    padded = f"{input:05}"
    return Modes(opcode= Opcode(int(padded[-2:])), 
                      mode1= int(padded[-3]), 
                      mode2=int(padded[-4]), 
                      mode3=int(padded[-5])) 

def problem_prep(problem_input: str) -> List[int]:
    inputs = [int(num) for num in problem_input.split(",")]
    return inputs

class Breakout: 
    def __init__(self, program: List[int]):
        self.program = defaultdict(lambda: 0) 
        self.program.update({pos:val for pos, val in enumerate(program)})
        self.pos = 0
        self.relative_base = 0
        self.outputs = deque()
        self.tiles_loc = {}

    def handle_mode(self, pos:int, mode: int) -> int:
        immediate_parameter = self.program[pos]
        if mode == 0 :
            # position mode
            return self.program[immediate_parameter]
        elif mode == 1:
            # immediate mode
            return  immediate_parameter
        elif mode == 2:
            # relative mode
            return self.program[immediate_parameter + self.relative_base] 
        else:
            raise ValueError(f"unknown mode: {mode} at pos {pos}")
    def _loc(self, pos: int, mode: int)-> int:
        """
        handles the writting instruction  either in position or relative mode only. 
        We need to know the loc where the value will be written to in the program
        """
        immediate_parameter = self.program[pos]
        if mode == 0:
            # position mode
            return immediate_parameter
        elif mode == 2:
            # relative mode
            return immediate_parameter + self.relative_base

    def handle_tiles_loc(self, outputs: List[int]) -> None:
        tileID = TilesID(outputs.pop())
        xy = XY(x = outputs.popleft() , y = outputs.pop())
        self.tiles_loc[xy] = tileID
    
    def handle_score(self, outputs: List[int]) -> int:
        score = outputs.pop()
        outputs.clear()
        return score
    
    def break_blocks(self, tiles_loc: Tiles_Loc ) -> None:
        ball_loc = self._get_ball_loc(tiles_loc)
        blocks_locs = self._get_blocks_locs(tiles_loc)
        if ball_loc in blocks_locs:
            del tiles_loc[ball_loc]
            tiles_loc[ball_loc] = TilesID.BALL
            return None

    def _get_blocks_locs(self, tiles_loc:Tiles_Loc) -> Set[XY]:
        return set(xy for xy, tile in tiles_loc.items() if tile == TilesID.BLOCK)

    def _get_ball_loc(self, tiles_loc:Tiles_Loc) -> Optional[XY]:
        ball_loc = [xy for xy, tile in tiles_loc.items() if tile == TilesID.BALL]
        if ball_loc:
            return ball_loc[0]
        else:
            return None

    def _get_paddle_loc(self, tiles_loc: Tiles_Loc) -> Optional[XY]:
        paddle_loc = [xy for xy, tile in tiles_loc.items() if tile == TilesID.PADDLE]
        if paddle_loc:
            return paddle_loc[0]
        else:
            return None
    
    def joystick_movement(self, tiles_loc: Dict[XY, TilesID] ) -> int:
        ball_loc = [xy for xy, tile in tiles_loc.items() if tile == TilesID.BALL][0]
        paddle_loc = [xy for xy, tile in tiles_loc.items() if tile == TilesID.PADDLE][0]
        if ball_loc.x <  paddle_loc.x: 
            return -1
        elif ball_loc.x > paddle_loc.x:
            return 1
        else:
            return 0

    def __call__(self, input: Optional[List[int]] ) -> EndProgram:
        """
        Programs takes an input, 9 + 1 opcodes are valid
        Parameter mode suport is available for 6 opcodes
        pointer(i) is incremented by the number of values in the instruction
        """
        self.score = 0
        self.step = 0 
        self.ball_exists = False


        if input:
            self.program[0] = input
        while True:
            modes = parse_opcode(self.program[self.pos])
            opcode = modes.opcode
            if self._get_ball_loc:
                self.ball_exists = True
            if self.ball_exists:# if there is a ball, start breaking 
                self.break_blocks(self.tiles_loc)
            if opcode == Opcode.PROGRAM_HALT:
                return EndProgram
            elif opcode == Opcode.ADD:
                num1 = self.handle_mode(self.pos + 1, modes.mode1)
                num2 = self.handle_mode(self.pos + 2, modes.mode2)
                loc = self._loc(self.pos + 3, modes.mode3)
                self.program[loc] = num1 + num2
                self.pos += 4
            elif opcode == Opcode.MULTIPLY:
                num1 = self.handle_mode(self.pos + 1, modes.mode1)
                num2 = self.handle_mode(self.pos + 2, modes.mode2)
                loc = self._loc(self.pos + 3, modes.mode3)
                self.program[loc] = num1 * num2
                self.pos += 4
            elif opcode == Opcode.JUMP_IF_TRUE:
                num1 = self.handle_mode(self.pos + 1, modes.mode1)
                num2 = self.handle_mode(self.pos + 2, modes.mode2)
                self.pos = num2 if num1 else self.pos + 3
            elif opcode == Opcode.JUMP_IF_FALSE: 
                num1 = self.handle_mode(self.pos + 1, modes.mode1)
                num2 = self.handle_mode(self.pos + 2, modes.mode2) 
                self.pos = num2 if not num1 else self.pos + 3
            elif opcode == Opcode.LESS_THAN: 
                num1 = self.handle_mode(self.pos + 1, modes.mode1)
                num2 = self.handle_mode(self.pos + 2, modes.mode2)
                loc = self._loc(self.pos + 3, modes.mode3)
                self.program[loc] = 1 if num1 < num2 else 0
                self.pos += 4
            elif opcode == Opcode.EQUALS: 
                num1 = self.handle_mode(self.pos + 1, modes.mode1)
                num2 = self.handle_mode(self.pos + 2, modes.mode2)
                loc = self._loc(self.pos + 3, modes.mode3)
                self.program[loc] = 1 if num1 == num2 else 0
                self.pos += 4
            elif opcode == Opcode.STORE_INPUT: 
                loc = self._loc(self.pos + 1, modes.mode1)
                curr_input = self.joystick_movement(self.tiles_loc)
                self.program[loc] = curr_input
                self.pos += 2
            elif opcode == Opcode.SEND_TO_OUTPUT:
                output = self.handle_mode(self.pos + 1, modes.mode1) 
                self.outputs.append(output)
                if len(self.outputs)== 3:
                    if self.outputs[0] == -1 and self.outputs[1] == 0:
                        self.score = self.handle_score(self.outputs)
                        # if we have a ball loc and count of all blocks is 0
                        if self.ball_exists and count_blocks(self.tiles_loc) == 0:
                            print('all blocks broken:: exiting program')
                            return self.score
                    else:
                        self.handle_tiles_loc(self.outputs)  
                self.pos += 2
            elif opcode == Opcode.ADJUST_RELATIVE_BASE:
                num1 = self.handle_mode(self.pos + 1, modes.mode1)
                self.relative_base += num1
                self.pos += 2
            else:
                raise RuntimeError(f"invalid opcode {opcode} at position {pos}")
            
            # if self.step > 1000 and self.step % 10 == 0:
            #      print(show_screen(self.tiles_loc))
            if self.ball_exists and self.step % 10000 == 0:
                print("num blocks", count_blocks(self.tiles_loc), "current score", self.score)
            self.step += 1

def count_blocks(tiles_loc: Tiles_Loc) -> int:
    return sum(1 for tile in tiles_loc.values() if tile == TilesID.BLOCK)

# PART 2

def get_screen(tiles_loc: Tiles_Loc)-> List[str]:
    col_min = min(x for x, y in tiles_loc.keys())
    col_max = max(x for x, y in tiles_loc.keys())
    row_min = min(y for x, y in tiles_loc.keys())
    row_max = max(y for x, y in tiles_loc.keys())

    screen = [[" " for _ in range (col_min, col_max + 1)] for _ in range(row_min, row_max + 1)]
    for row in range(row_min, row_max + 1):
        for col in range(col_min, col_max + 1):
            tile = tiles_loc.get((col, row), TilesID.EMPTY)
            if tile.name == 'EMPTY':
                continue
            elif tile.name == 'WALL':
                screen[row][col] = "%"
            elif tile.name == 'BLOCK':
                screen[row][col] = "\u2588"
            elif tile.name == 'PADDLE':
                screen[row][col] = "#"
            elif tile.name == 'BALL':
                screen[row][col] = 'O'
    return screen


def show_screen(tiles_loc: Tiles_Loc)-> str:
    screen = get_screen(tiles_loc)
    image = []
    for row in screen:
        image.append("".join(row))
    return "\n".join(image)

"""
At game start:
    first Input - Memory address 0 represents the number of quarters that have been inserted; set it to 2 to play for free
    - run intcode 
        - maybe or not during first program run:
            - move Joystick based on instruction STORE_INPUT
                - if ball column left to horiz paddle provide -1
                - right 1 same 0
        - if at any given point the ball IJ is in the blocks IJ, pop out
        - segment display -> current score, if win the 3 outputs queue
            - X = -1 and Y = 0, last output is the score  
"""

if __name__ == "__main__":
    with open("day13_puzzle_input.txt", 'r') as file:
        PUZZLE_INPUT = problem_prep(file.read())
        # part1 = Breakout(program=PUZZLE_INPUT)
        breakout = Breakout(PUZZLE_INPUT)
        breakout(input = 2)
        print("score when all blocks are broken", breakout.score)


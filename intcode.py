from typing import NamedTuple, List
from enum import Enum
from collections import deque, defaultdict

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

class EndProgram(Exception): pass

def parse_opcode(input: int) -> Modes:
    padded = f"{input:05}"
    return Modes(opcode= Opcode(int(padded[-2:])), 
                      mode1= int(padded[-3]), 
                      mode2=int(padded[-4]), 
                      mode3=int(padded[-5])) 

def problem_prep(problem_input: str) -> List[int]:
    inputs = [int(num) for num in problem_input.split(",")]
    return inputs

class Intcode: # inspired by Joel Grus Intocode computer
    def __init__(self, program: List[int]):
        self.program = defaultdict(lambda: 0) 
        self.program.update({pos:val for pos, val in enumerate(program)})
        self.pos = 0
        self.relative_base = 0
        self.outputs = []
        self.inputs = deque()

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

    # from here
    def __call__(self, input: List[int]) -> EndProgram:
        """
        Programs takes an input, 9 + 1 opcodes are valid
        Parameter mode suport is available for 6 opcodes
        pointer(i) is incremented by the number of values in the instruction
        """
        self.inputs.extend(input)
        while True:
            modes = parse_opcode(self.program[self.pos])
            opcode = modes.opcode
            if opcode == Opcode.PROGRAM_HALT:
                print('halting program')
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
                #print(f'param1 {num1}, param2 {num2}')
                self.pos = num2 if num1 else self.pos + 3
            elif opcode == Opcode.JUMP_IF_FALSE: 
                num1 = self.handle_mode(self.pos + 1, modes.mode1)
                num2 = self.handle_mode(self.pos + 2, modes.mode2) 
                #print(f'param1 {num1}, param2 {num2}')
                self.pos = num2 if not num1 else self.pos + 3
            elif opcode == Opcode.LESS_THAN: 
                num1 = self.handle_mode(self.pos + 1, modes.mode1)
                num2 = self.handle_mode(self.pos + 2, modes.mode2)
                loc = self._loc(self.pos + 3, modes.mode3)
                #print(f'param1 {num1}, param2 {num2}, param3 {loc}')
                self.program[loc] = 1 if num1 < num2 else 0
                self.pos += 4
            elif opcode == Opcode.EQUALS: 
                num1 = self.handle_mode(self.pos + 1, modes.mode1)
                num2 = self.handle_mode(self.pos + 2, modes.mode2)
                loc = self._loc(self.pos + 3, modes.mode3)
                #print(f'param1 {num1}, param2 {num2}, param3 {loc}')
                self.program[loc] = 1 if num1 == num2 else 0
                self.pos += 4
            elif opcode == Opcode.STORE_INPUT: 
                loc = self._loc(self.pos + 1, modes.mode1)
                #print(f'param1 {num1}')
                curr_input = self.inputs.popleft()
                self.program[loc] = curr_input
                self.pos += 2
            elif opcode == Opcode.SEND_TO_OUTPUT:
                output = self.handle_mode(self.pos + 1, modes.mode1) 
                self.outputs.append(output)
                self.pos += 2
            elif opcode == Opcode.ADJUST_RELATIVE_BASE:
                num1 = self.handle_mode(self.pos + 1, modes.mode1)
                #print(f'param1 {num1}')
                self.relative_base += num1
                #print('in relative base, adjusted to' , relative_base) 
                self.pos += 2
            else:
                raise RuntimeError(f"invalid opcode {opcode} at position {pos}")
            return None    


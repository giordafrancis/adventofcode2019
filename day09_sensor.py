"""
https://adventofcode.com/2019/day/9
"""

from typing import List, NamedTuple, Optional
from enum import Enum
from collections import deque
import logging

logging.basicConfig(level=logging.DEBUG)

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

def parse_opcode2(opcode: int, num_modes: int = 3) -> Modes:
    """
    By joel grus code
    how to handle modes without parsing to a str
    """
    opcode_part = opcode % 100
    modes: List[int] = []
    opcode = opcode // 100

    for _ in range(num_modes):
        modes.append(opcode % 10)
        opcode = opcode // 10
    return Modes(opcode = Opcode(opcode_part),
                 mode1= modes[0],
                 mode2= modes[1],
                 mode3= modes[2])

def parse_opcode(input: int) -> Modes:
    padded = f"{input:05}"
    return Modes(opcode= Opcode(int(padded[-2:])), 
                      mode1= int(padded[-3]), 
                      mode2=int(padded[-4]), 
                      mode3=int(padded[-5]))  

def problem_prep(problem_input: str) -> List[int]:
    inputs = [int(num) for num in problem_input.split(",")]
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
    handles the writting instructionwither in position or relative mode only. 
    We need to know the loc where the value will be written to in the program
    """
    immediate_parameter = program[pos]
    if mode == 0:
        # position mode
        return immediate_parameter
    elif mode == 2:
        # relative mode
        return immediate_parameter + relative_base



def run_intcode(program: List[int], inputs:int=[1]) -> List[int]:
    """
    Programs takes an input, 9 + 1 opcodes are valid
    Parameter mode suport is available for 6 opcodes
    pointer(i) is incremented by the number of values in the instruction
    """
    program = program[:]
    inputs = deque(inputs)
    for _ in range(10000):
        program.append(0)  # add program large memory, lazy solution
    outputs = []
    pos = relative_base =  0
    
    while True:
        #print('pos prior to opcode parse',pos)
        modes = parse_opcode(program[pos])
        opcode = modes.opcode
        #print(f'modes are {modes}')
        #print(program[:20])
        if opcode == Opcode.PROGRAM_HALT: 
            break
        elif opcode == Opcode.ADD:
            num1 = handle_mode(program, pos + 1, modes.mode1, relative_base)
            num2 = handle_mode(program, pos + 2, modes.mode2, relative_base)
            loc = _loc(program, pos + 3, modes.mode3, relative_base)
            #print(f'param1 {num1}, param2 {num2}, param3 {loc}')
            program[loc] = num1 + num2        
            pos += 4
        elif opcode == Opcode.MULTIPLY: 
            num1 = handle_mode(program, pos + 1, modes.mode1, relative_base)
            num2 = handle_mode(program, pos + 2, modes.mode2, relative_base)
            loc = _loc(program, pos + 3, modes.mode3, relative_base)
            #print(f'param1 {num1}, param2 {num2}, param3 {loc}')
            program[loc] = num1 * num2
            pos += 4
        elif opcode == Opcode.JUMP_IF_TRUE:
            num1 = handle_mode(program, pos + 1, modes.mode1, relative_base)
            num2 = handle_mode(program, pos + 2, modes.mode2, relative_base)
            #print(f'param1 {num1}, param2 {num2}')
            pos = num2 if num1 else pos + 3
        elif opcode == Opcode.JUMP_IF_FALSE: 
            num1 = handle_mode(program, pos + 1, modes.mode1, relative_base)
            num2 = handle_mode(program, pos + 2, modes.mode2, relative_base) 
            #print(f'param1 {num1}, param2 {num2}')
            pos = num2 if not num1 else pos + 3
        elif opcode == Opcode.LESS_THAN: 
            num1 = handle_mode(program, pos + 1, modes.mode1, relative_base)
            num2 = handle_mode(program, pos + 2, modes.mode2, relative_base)
            loc = _loc(program, pos + 3, modes.mode3, relative_base)
            #print(f'param1 {num1}, param2 {num2}, param3 {loc}')
            program[loc] = 1 if num1 < num2 else 0
            pos += 4
        elif opcode == Opcode.EQUALS: 
            num1 = handle_mode(program, pos + 1, modes.mode1, relative_base)
            num2 = handle_mode(program, pos + 2, modes.mode2, relative_base)
            loc = _loc(program, pos + 3, modes.mode3, relative_base)
            #print(f'param1 {num1}, param2 {num2}, param3 {loc}')
            program[loc] = 1 if num1 == num2 else 0
            pos += 4
        elif opcode == Opcode.STORE_INPUT: 
            loc = _loc(program, pos + 1, modes.mode1, relative_base)
            #print(f'param1 {num1}')
            curr_input = inputs.popleft()
            program[loc] = curr_input
            pos += 2
        elif opcode == Opcode.SEND_TO_OUTPUT:
            output = handle_mode(program, pos + 1, modes.mode1, relative_base) 
            outputs.append(output)
            pos += 2
        elif opcode == Opcode.ADJUST_RELATIVE_BASE:
            num1 = handle_mode(program, pos + 1, modes.mode1, relative_base)
            #print(f'param1 {num1}')
            relative_base += num1
            #print('in relative base, adjusted to' , relative_base) 
            pos += 2
        else:
            raise RuntimeError(f"invalid opcode {opcode} at position {pos}")
    return outputs


# TEST1 = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
# print(run_intcode(TEST1))
# TEST1 = [1102,34915192,34915192,7,4,7,99,0]
# print(run_intcode(TEST1))
# TEST1 = [104,1125899906842624,99]
# print(run_intcode(TEST1))

if __name__ == "__main__":
    with open("day09_puzzle.txt", 'r') as file:
        program = problem_prep(file.read())
        part1 = run_intcode(program=program)
        part2 = run_intcode(program=program, inputs=[2])
        print('part 1 test mode',part1)
        print('part 2 sensor boost mode',part2)


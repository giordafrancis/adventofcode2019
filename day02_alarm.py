"""
https://adventofcode.com/2019/day/2
"""

from typing import List, NamedTuple, Iterator
import itertools

class Command(NamedTuple):
    pointer: int
    opcode: int
    pos_1: int
    pos_2: int
    pos_final: int

def instructions(inputs: List[int]) -> Iterator[Command]:
    """
    Splits instructions into Commands based on opcodes 1, 2 & 99
    """
    length = len(inputs)
    for i in range(0, length, 4):
        opcode = inputs[i]
        if opcode == 99:
            yield Command(pointer=i, opcode=opcode, pos_1=None, pos_2=None, pos_final=None)
        else:
            yield Command(pointer=i, opcode=opcode, pos_1=inputs[i + 1] , pos_2=inputs[i + 2], pos_final=inputs[i + 3])
            
TEST_INPUT = [1,9,10,3,2,3,11,0,99,30,40,50]

def intcode(inputs: List[int], noun:int=0, verb:int=0) -> None:
    """
    Return value at position 0 once 
    opcode 99 is found. 
    """
    inputs = inputs.copy() # required for part 2
    inputs[1] = noun # as defined in the problem noun & verb inputs
    inputs[2] = verb 
    commands = instructions(inputs)
    for command in commands:
        if command.opcode == 99:
            return inputs[0]
        elif command.opcode == 1:
             inputs[command.pos_final] = inputs[command.pos_1] + inputs[command.pos_2]
        elif command.opcode == 2:
             inputs[command.pos_final] = inputs[command.pos_1] * inputs[command.pos_2]
        else:
            raise RuntimeError(f"invalid opcode {command.opcode}")
    
assert intcode(TEST_INPUT, noun=TEST_INPUT[1], verb=TEST_INPUT[2]) == 3500

def problem_prep(problem_input: str, noun:int = 0, verb:int = 0) -> List[int]:
    inputs = [int(num) for num in problem_input.split(",")]
    return inputs

# PART 2

def inputs_brute_force(inputs: List[int]) -> int:
    """
    finds the input pairs between 0 - 99 inclusive 
    that produce an output of 19690720
    """
    input_pairs = itertools.permutations(range(0,100), 2) # pairs between 0 and 99 inclusive
    while True:
        noun, verb = next(input_pairs)
        if intcode(inputs, noun=noun, verb=verb) == 19690720:
            return 100 * noun + verb
            break

if __name__ == "__main__":
    with open("day02_inputs.txt") as file:
        problem_input = file.read()
        inputs = problem_prep(problem_input, noun=12, verb=2)
        part_1 = intcode(inputs, noun=12, verb=2)
        part_2 = inputs_brute_force(inputs)
        print("PART 1 halt code pos 0->",part_1)
        print("PART 2 value based on input pairs is->",part_2)























































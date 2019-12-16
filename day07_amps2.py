"""
Full disclaimer: I did not resolve part 2, mixture of not intrepreing the problem correctly and the nightamre of keeping the program state in between amplifiers and resuming 
at the correct ponint
As Joel Grus solution was apealing  to me on how to use classes for this.  
"""



from typing import Iterator, Generator, Tuple, List, NamedTuple
from intcode import problem_prep, Parameters, Instructions
from enum import Enum
import itertools
import logging
from collections import deque

logging.basicConfig(level=logging.INFO)

# Enum for machine with set states
class Opcode(Enum): 
    ADD = 1
    MULTIPLY = 2
    STORE_INPUT = 3
    SEND_TO_OUTPUT = 4
    JUMP_IF_TRUE = 5 
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    PROGRAM_HALT = 99

    def parameter_support(self):
        return True if self.value in (1,2,5,6,7,8) else False

def parse_opcode(input: int) -> Parameters:
    padded = f"{input:05}"
    return Parameters(opcode= Opcode(int(padded[-2:])), 
                      mod1= int(padded[-3]), 
                      mod2=int(padded[-4]), 
                      mod3=int(padded[-5]))   

def parse_instructions2(pos:int, program:List[int])-> Instructions:
    params = parse_opcode(program[pos])
    opcode = params.opcode
    if opcode == Opcode.PROGRAM_HALT or opcode == Opcode.SEND_TO_OUTPUT:
        return Instructions(parameters = params)
    elif opcode == Opcode.JUMP_IF_TRUE or  opcode == Opcode.JUMP_IF_FALSE:
        return Instructions(parameters = params,
                            val1=program[pos + 1],
                            val2 =program[pos + 2])
    else:
        return Instructions(parameters=params,
                            val1=program[pos + 1],
                            val2=program[pos + 2],
                            val3=program[pos + 3])


Modes = List[int]
Program = List[int]

class EndProgram(Exception):
    """Not implemented""" 
    pass
    

def get_phase_settings(arange:Iterator[int]=range(5,10), size:int=5) -> Generator:
    parameters = itertools.permutations(arange, size)
    for p in parameters:
        yield p

class Amplifier:
    """ Amplifier is a machine that needs to keep its state
    Phase provided to Amplifier once only for 5 amps
    position and program is kept for each iteration
    """
    def __init__(self, program: Program, phase: int) -> None:
        self.program = program[:]
        self.inputs = deque([phase])
        self.pos = 0

    def _get_value(self, pos: int, mode: int)-> int:
        if mode == 0 :
            # pointer mode
            return self.program[self.program[pos]]
        elif mode == 1:
            # immediate mode
            return self.program[pos]
        else:
            raise ValueError(f"unknown mode: {mode}")

    def __call__(self, input_value: int) -> int:
        self.inputs.append(input_value)
        while True:
            inst = parse_instructions2(self.pos, self.program)
            opcode = inst.parameters.opcode
            params = inst.parameters
            logging.debug(f"pos: {self.pos}, opcode {opcode}, params: {params}")
            if opcode == Opcode.PROGRAM_HALT: # stop 
                return EndProgram
            # params mode support immediate == 1 or position == 0  
            elif opcode.parameter_support():
                num1 = self._get_value(self.pos + 1, params.mod1)
                num2 = self._get_value(self.pos + 2, params.mod2)                
                if opcode == Opcode.ADD: #add
                    self.program[inst.val3] = num1 + num2 #write to always in position
                    self.pos += 4
                elif opcode == Opcode.MULTIPLY: #mul
                    self.program[inst.val3] = num1 * num2
                    self.pos += 4
                elif opcode == Opcode.JUMP_IF_TRUE: # pointer jump if true 
                    self.pos = num2 if num1 else self.pos + 3
                elif opcode == Opcode.JUMP_IF_FALSE: # pointer jump if False
                    self.pos = num2 if not num1 else self.pos + 3
                elif opcode == Opcode.LESS_THAN: # less than
                    self.program[inst.val3] = 1 if num1 < num2 else 0
                    self.pos += 4
                elif opcode == Opcode.EQUALS: # equals
                    self.program[inst.val3] = 1 if num1 == num2 else 0
                    self.pos += 4
                else:
                    raise ValueError(f'unknown opcode{opcode} for param support at {self.pos}')
            elif opcode == Opcode.STORE_INPUT:
                curr_input = self.inputs.popleft()
                self.program[inst.val1] = curr_input  # systems ID
                self.pos += 2
            elif opcode == Opcode.SEND_TO_OUTPUT:
                # Get output from location
                output = self._get_value(self.pos + 1, params.mod1)
                self.pos += 2
                return output
            else:
                raise ValueError(f'unknown opcode{opcode} for  at {self.pos}')
                

def run_amplifiers(program: List[int], phases: List[int]) -> int:
    amplifiers = deque([Amplifier(program, phase) for phase in phases])
    output = 0

    last_valid_output = None # could not implement try and except block
    while amplifiers:
        amplifier = amplifiers.popleft()
        output = amplifier(output)
        if output is EndProgram:
            pass
        else:
            last_valid_output = output
            amplifiers.append(amplifier)
    return last_valid_output

def run_amplifiers2(program: List[int], phases: List[int]) -> int:
    amplifiers = deque([Amplifier(program, phase) for phase in phases])
    output = 0

    # try except capture not fully working 
    while amplifiers:
        amplifier = amplifiers.popleft()

        try:
            output = amplifier(output)
            amplifiers.append(amplifier)
        except EndProgram:
            pass
    return output

    
PROG1 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
PHASES1 = [9,8,7,6,5]
assert run_amplifiers(PROG1, PHASES1) == 139629729

PROG1 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
PHASES1 = [9,7,8,5,6]
assert run_amplifiers(PROG1, PHASES1) == 18216

def max_output(program: Program, phases_range:Tuple[int]= (5,10))-> int:
    bottom, top = phases_range
    return max(run_amplifiers(program, phases) for 
            phases in itertools.permutations(range(bottom,top)))

PROG1 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
assert max_output(PROG1) == 139629729

PROG1 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
assert max_output(PROG1) == 18216

if __name__ == "__main__":
    with open("day07_input.txt", 'r') as file:
        program = problem_prep(file.read())
        part2 = max_output(program = program)
        print("max signal in feedback loop: part2", part2)












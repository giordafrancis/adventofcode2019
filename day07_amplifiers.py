from intcode import parse_instructions2, problem_prep
from typing import Iterator, Generator, Tuple, List, NamedTuple
import itertools

class OutputParams(NamedTuple):
    final_output: int
    parameters: Tuple[int]

def get_phase_settings(arange:Iterator[int]=range(5), size:int=5) -> Generator:
    parameters = itertools.permutations(arange, size)
    for p in parameters:
        yield p

def run_amplifier(intcode: List[int], inputs:List[int]) -> List[int]:
    """
    Programs takes an input, 8 + 1 opcodes are valid
    Parameter mode suport is available for 6 opcodes
    pointer(i) is incremented by the number of values in the instruction
    """
    intcode = intcode[:] # don't destroy intcode
    outputs = []
    opcode = i = 0
    while True:
        inst = parse_instructions2(i,intcode)
        opcode = inst.parameters.opcode
        params = inst.parameters
        #print('opcode is', opcode)
        if opcode == 99: # stop 
            break
        # params mode support immediate == 1 or position == 0  
        elif opcode == 1 or opcode == 2 or opcode == 5 or opcode == 6 or opcode == 7 or opcode == 8: 
            num1 = inst.val1 if params.mod1 == 1 else intcode[inst.val1]
            num2 = inst.val2 if params.mod2 == 1 else intcode[inst.val2]
            if opcode == 1: #add
                intcode[inst.val3] = num1 + num2 #write to always in position
                i += 4
            elif opcode == 2: #mul
                intcode[inst.val3] = num1 * num2
                i += 4
            elif opcode == 5: # pointer jump if true 
                i = num2 if num1 else i + 3
            elif opcode == 6: # pointer jump if False
                i = num2 if not num1 else i + 3
            elif opcode == 7: # less than
                intcode[inst.val3] = 1 if num1 < num2 else 0
                i += 4
            elif opcode == 8: # equals
                intcode[inst.val3] = 1 if num1 == num2 else 0
                i += 4
        elif opcode == 3: # input
            curr_input = inputs[0]
            print(curr_input)
            inputs = inputs[1:]
            intcode[inst.val1] = curr_input  # systems ID
            i += 2
        elif opcode == 4:
            output = intcode[inst.val1]
            outputs.append(output)
            i += 2
        else:
            raise RuntimeError(f"invalid opcode {opcode} at position {i}")
    return outputs

def amp_to_thruster(intcode: List[int], num_amps:int=5) -> int:
    """
     Calls intcode on amp1, input 1 & 2 ->  output  on amp2, setting2 ..
     returns 
    """
    intcode = intcode[:]
    input1 = 0
    final_outputs = set()
    for params in get_phase_settings(arange=range(num_amps), size=num_amps): 
        #print(params)
        for amp_num, p in enumerate(params):
            #print('at amp->',amp_num, 'using param->',p)
            if amp_num == 0:
                inputs = [p, input1]
                output  = run_amplifier(intcode, inputs)[0]
            elif amp_num == 4:
                inputs = [p, output]
                final_output = run_amplifier(intcode, inputs)[0]
            else:
                inputs = [p, output]
                output = run_amplifier(intcode, inputs)[0]       
        final_outputs.add(OutputParams(final_output=final_output,
                                            parameters=params))
    return max(final_outputs)
            
    
TEST_INTCODE = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
assert amp_to_thruster(num_amps=5, intcode=TEST_INTCODE).final_output == 54321
assert amp_to_thruster(num_amps=5, intcode=TEST_INTCODE).parameters == (0,1,2,3,4)

TEST_INTCODE = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
assert amp_to_thruster(num_amps=5, intcode=TEST_INTCODE).final_output == 43210
assert amp_to_thruster(num_amps=5, intcode=TEST_INTCODE).parameters == (4,3,2,1,0)

TEST_INTCODE = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
assert amp_to_thruster(num_amps=5, intcode=TEST_INTCODE).final_output == 65210
assert amp_to_thruster(num_amps=5, intcode=TEST_INTCODE).parameters == (1,0,4,3,2)

#PART 2


# TEST_INTCODE = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
# 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
# assert amp_to_thruster_loop(intcode=TEST_INTCODE).final_output == 139629729
# assert amp_to_thruster_loop(intcode=TEST_INTCODE).parameters == (9,8,7,6,5)

if __name__ == "__main__":
    with open("day07_input.txt", 'r') as file:
        intcode = problem_prep(file.read())
        # part1 = amp_to_thruster(intcode=intcode, num_amps=5)
        # print("max signal and params to trusters", part1)

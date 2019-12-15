from typing import NamedTuple, List, Iterator

class Parameters(NamedTuple):
    opcode: int
    mod1: int
    mod2: int
    mod3: int

class Instructions(NamedTuple):
    parameters: Parameters
    val1: int = None
    val2: int = None
    val3: int = None


def parse_params(input: int) -> Parameters:
    padded = f"{input:05}"
    return Parameters(opcode= int(padded[-2:]), 
                      mod1= int(padded[-3]), 
                      mod2=int(padded[-4]), 
                      mod3=int(padded[-5]))   

def problem_prep(problem_input: str) -> List[int]:
    inputs = [int(num) for num in problem_input.split(",")]
    return inputs

def parse_instructions2(i:int, inputs:List[int])-> Instructions:
    params = parse_params(inputs[i])
    opcode = params.opcode
    if opcode == 99:
        return Instructions(parameters = params)
    elif opcode == 5 or opcode == 6:
        return Instructions(parameters = params,
                            val1=inputs[i + 1],
                            val2 =inputs[i + 2])
    else:
        return Instructions(parameters = params,
                            val1=inputs[i + 1],
                            val2=inputs[i + 2],
                            val3=inputs[i + 3])


def intcode(inputs: List[int], ID:List[int]) -> List[int]:
    """
    Programs takes an input, 8 + 1 opcodes are valid
    Parameter mode suport is available for 6 opcodes
    pointer(i) is incremented by the number of values in the instruction
    """
    inputs = inputs[:] # don't destroy inputs
    outputs = []
    opcode = i = 0
    while True:
        inst = parse_instructions2(i,inputs)
        opcode = inst.parameters.opcode
        params = inst.parameters
        if opcode == 99: # stop 
            break
        # params mode support immediate == 1 or position == 0  
        elif opcode == 1 or opcode == 2 or opcode == 5 or opcode == 6 or opcode == 7 or opcode == 8: 
            num1 = inst.val1 if params.mod1 == 1 else inputs[inst.val1]
            num2 = inst.val2 if params.mod2 == 1 else inputs[inst.val2]
            if opcode == 1: #add
                inputs[inst.val3] = num1 + num2 #write to always in position
                i += 4
            elif opcode == 2: #mul
                inputs[inst.val3] = num1 * num2
                i += 4
            elif opcode == 5: # pointer jump if true 
                i = num2 if num1 else i + 3
            elif opcode == 6: # pointer jump if False
                i = num2 if not num1 else i + 3
            elif opcode == 7: # less than
                inputs[inst.val3] = 1 if num1 < num2 else 0
                i += 4
            else: #opcode == 8: # equals
                inputs[inst.val3] = 1 if num1 == num2 else 0
                i += 4
        elif opcode == 3: # input
            inputs[inst.val1] = inputs[0] # systems ID
            i += 2
            
            
        elif opcode == 4:
            output = inputs[inst.val1]
            outputs.append(output)
            i += 2
        else:
            raise RuntimeError(f"invalid opcode {opcode} at position {i}")
    return outputs

    if __name__ == "__main__":
        with open("day05_inputs.txt", 'r') as file:
            inputs = problem_prep(file.read())
            #part1 = intcode(inputs, ID=1)
            part2 = intcode2(inputs, ID=[5,0])
            print(part1)
            print(part2)

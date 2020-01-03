"""
My second attempt using OOP for day09
"""
import intcode
from typing import NamedTuple, List


def run_sensor(program: List[int], input : List[int] = [1]) -> List[int]:
    sensor = intcode.Intcode(program)
    while True:
        sensor(input = input) 
        if intcode.EndProgram:
            return sensor.outputs

TEST1 = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
assert run_sensor(TEST1) == TEST1
TEST1 = [1102,34915192,34915192,7,4,7,99,0]
assert len([val for val in str(run_sensor(TEST1)[0])]) == 16 
TEST1 = [104,1125899906842624,99]
assert run_sensor(TEST1)[0] == TEST1[1]

if __name__ == "__main__":
    with open("day09_puzzle.txt", 'r') as file:
        program = intcode.problem_prep(file.read())
        part1 = run_sensor(program=program, input=[1])
        part2 = run_sensor(program=program, input=[2])
        print('part 1 test mode',part1)
        print('part 2 sensor boost mode',part2)
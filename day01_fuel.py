"""
https://adventofcode.com/2019/day/1
"""


def module_fuel(module: int) -> int:
    return module // 3 - 2

assert module_fuel(12) == 2
assert module_fuel(14) == 2
assert module_fuel(1969) == 654
assert module_fuel(100756) == 33583

def required_fuel(module: int) -> int:

    fuel = module_fuel(module)
    total_fuel = 0 

    while fuel > 0:
        total_fuel += fuel
        fuel = module_fuel(fuel)
    return total_fuel

assert required_fuel(14) == 2
assert required_fuel(1969) == 966
assert required_fuel(100756) == 50346

if __name__ == "__main__":
     with open("day01_input.txt") as file:
        modules = file.readlines()
        part_1 = sum(module_fuel(int(module))
                    for module in modules)
        part_2 = sum(required_fuel(int(module))
                    for module in modules)
        print("Part 1 total module fuel->", part_1)
        print("Part 2 total required fuel->", part_2)


    

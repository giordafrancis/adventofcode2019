"""
https://adventofcode.com/2019/day/4
"""

from typing import List
from collections import Counter

INPUT = (367479, 893698)

def never_decreases(digits: List[int])-> bool:
    return all(num1 <= num2 for num1, num2 in zip(digits, digits[1:]))

def least_one_pair(digits: List[int])-> bool:
    return any(num1 == num2 for num1, num2 in zip(digits, digits[1:]))

def is_valid(inputs = INPUT) -> int:
    low, high = INPUT
    for num in range(low, high + 1):
        digits = [int(n) for n in str(num)]
        if never_decreases(digits) and least_one_pair(digits):
            yield True

# Part 2 

def has_group_two(digits: List[int])-> bool:
    count = Counter(digits)
    return any(val == 2 for val in count.values())

def is_valid2(inputs = INPUT) -> int:
    low, high = INPUT
    for num in range(low, high + 1):
        digits = [int(n) for n in str(num)]
        if never_decreases(digits) and has_group_two(digits):
            yield True

assert has_group_two([1,1,2,2,3,3]) 
assert not has_group_two([1,2,3,4,4,4]) 
assert has_group_two([1,1,1,1,2,2]) 

if __name__ == "__main__":
    part_1 = sum(is_valid())
    part_2 = sum(is_valid2())
    print("total number of passwords part1 ->", part_1)
    print("total number of passwords part2 ->", part_2)


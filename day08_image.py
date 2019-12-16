"""
https://adventofcode.com/2019/day/8
"""

from typing import List, Tuple, NamedTuple, Iterator
import itertools
import math

Layer = Tuple[Tuple[int]]

class LayerMetrics(NamedTuple):
    name: str
    count: int
    layer_nums: Layer

def grouper(iterable: List[int], size:int) -> Iterator[Tuple[int]]:
    iterable = iter(iterable)
    while True:
        tup = tuple(itertools.islice(iterable, 0, size))
        if tup:
            yield tup
        else:
            break

def get_layer(inputs: List[int], width:int, height:int, dig_count: int) -> Iterator[Layer]:
    batches = grouper(inputs, width)
    layers = grouper(batches, height)
    for i, layer in enumerate(layers,1):
        yield LayerMetrics(name = f'Layer_{i}',
                     count = count_digits(layer, dig_count),
                     layer_nums= layer) 
        
def result_part1(inputs: List[int], width:int, height:int, dig_count:int) -> int:
    
    min_result  = math.inf
    result  = None
    for layer in get_layer(inputs, width, height, dig_count):
        if layer.count < min_result:
            min_result = layer.count
            result = mult_digits(layer.layer_nums, 1, 2) # hardcoded for now
    return result

def count_digits(layer: Layer, digit:int)-> int:
    count = 0
    for l in layer:
        for d in l:
            if d == digit:
                count += 1
    return count

def mult_digits(layer: Layer, digit1:int, digit2: int)-> int:
    count_1 = count_digits(layer, digit1)
    count_2 = count_digits(layer, digit2)
    return count_1 * count_2

def problem_prep(text_input:str)-> List[int]:
    return [int(s) for s in text_input.strip()]
    

TEST1 = [0,0,3,4,5,6,1,8,9,0,1,2]
assert result_part1(TEST1, width=3, height=2, dig_count=0) == 2

# TEST1 = ((1, 8, 9), (0, 1, 2))
# print(count_digits(TEST1, digit=0))
# print(mult_digits(TEST1, digit1=1, digit2=2))

if __name__ == "__main__":
    with open("day08_input.txt", 'r') as file:
        inputs = problem_prep(file.read())
        part1 = result_part1(inputs, width=25, height=6, dig_count=0)
        print("1s multiply the 2s in fewest 0s layer", part1)


    


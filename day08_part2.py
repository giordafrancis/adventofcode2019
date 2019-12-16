"""
https://adventofcode.com/2019/day/8
"""

from typing import List, Iterator
from day08_image import problem_prep
import itertools
import copy

Layer = List[List[int]]

def grouper(iterable: List[int], size:int) -> Iterator[List[int]]:
    iterable = iter(iterable)
    while True:
        batch = list(itertools.islice(iterable, 0, size))
        if batch:
            yield batch
        else:
            break

TEST1 = [0,2,2,2,1,1,2,2,2,2,1,2,0,0,0,0]
TEST2 = [1,2,3,4,5,6,7,8,9,0,1,2]
# print(list(grouper(TEST1, 2)))
# print(list(grouper(TEST2,3)))

def pixel_comparison(inputs: List[int], width:int, rows:int) -> List[int]:
    """
    Compares top layer pixels and transforms it based on 
    transparent
    """
    # review layer by layer but on flat list
    flat_layers = list(grouper(inputs, width * rows)) 
    top_layer = copy.deepcopy(flat_layers[0]) 
    #print('initial top layer', top_layer)
    L  = len(top_layer)
    i = 0
        
    for _ in range(L):
        color = top_layer[i]
        for layer in flat_layers[1:]:
            #print(f'current color is {color}, at layer {layer} layer[i] is {layer[i]}', f'::: index is at {i}')
            if color == 2:
                color = layer[i]
                #print(f'color changed from 2 to {layer[i]}')
                top_layer[i] = color
                continue
            elif color == 1 or color == 0:
                #print(f'color is {color} breaking the loop')
                break
        #print('current top layer', top_layer)
        i += 1
    #print('final top layer', top_layer)      
    return top_layer

def get_image(top_layer: List[int], width: int, rows: int)-> List[List[str]]:
    layer = list(grouper(top_layer, width))
    image_layer = copy.deepcopy(layer)
    #print(f'current image layer is {image_layer}')
    color = None
    for i in range(rows):
        for j in range(width):
            #print('row is', i, 'col is',j)
            color = image_layer[i][j]
            if color == 0:
                image_layer[i][j] = "X"
            else:
                image_layer[i][j] = " "
    return image_layer

def print_image(top_layer: List[int], width: int, rows: int)-> str:
    image_layer = get_image(top_layer, width, rows)
    image = []
    for row in image_layer:
        image.append("".join(row))
    return "\n".join(image)
        
    
if __name__ == "__main__":
    with open("day08_input.txt", 'r') as file:
        inputs = problem_prep(file.read())
        part2 = pixel_comparison(inputs, width=25, rows=6)
        print(print_image(part2,width= 25, rows= 6))





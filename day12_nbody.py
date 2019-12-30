"""
https://adventofcode.com/2019/day/12
"""

"""
objective: calculate the position of each moon (your puzzle input). You just need to simulate their motion so you can avoid them.

- each has a 3 dimensional position and a 3 dimensional velocity
- simulate the motions in time steps (epochs)
    - within each epoch:
        - first update the velocity by applying gravity
        - second update the position by applying the velocity

- to apply gravity
    - velocity axis changes of each moon by exactly +1 or -1  based on position axis. if the same no change
    - once all gravity has been update apply velocity
- apply velocity:
    - simply add each velocity axis to it's position axis. 
"""

from typing import Dict, NamedTuple, Pattern, Tuple
import re
import itertools
import math


class Position(NamedTuple):
    x: int
    y: int
    z: int

class Velocity(NamedTuple):
    vx: int = 0
    vy: int = 0
    vz: int = 0

class Moon(NamedTuple):
    position: Position
    velocity: Velocity
    
patt = re.compile("<x=(?P<x>[-?0-9]+), y=(?P<y>[-?0-9]+), z=(?P<z>[-?0-9]+)>")

def problem_prep(pattern: Pattern, puzzle_input: str) -> Dict[str,Moon]:
    inputs = puzzle_input.strip().split('\n')
    output = {}

    for i, pos in enumerate(inputs):
        g = pattern.search(pos)
        x, y, z = g.group('x'), g.group('y'), g.group('z')
        moon_pos = Position(x= int(x), y=int(y), z= int(z))
        moon_vel = Velocity()
        name = f"moon_{i}"
        output[name] = Moon(position = moon_pos,
                            velocity= moon_vel)
    return output

def run_epochs(moons: Dict[str,Moon], num_epochs:int =1000) -> Dict[str, Moon]:

    steps = 0
    while steps < num_epochs:
        moon_pairs = itertools.combinations(moons.keys(), 2)
        for m0,m1 in moon_pairs:
            moon0 = moons[m0]
            moon1 = moons[m1]
            vx0, vy0 , vz0 = moon0.velocity
            vx1, vy1 , vz1 = moon1.velocity
            x0, y0, z0 = moon0.position
            x1, y1, z1 = moon1.position
            
            #apply gravity
            if x0 == x1:
                pass
            elif x0 < x1:
                vx0 +=  1
                vx1 -= 1
            else: 
                vx1 +=  1
                vx0 -= 1

            if y0 == y1:
                pass
            elif y0 < y1:
                vy0 +=  1
                vy1 -= 1
            else: 
                vy1 +=  1
                vy0 -= 1
            
            if z0 == z1:
                pass
            elif z0 < z1:
                vz0 +=  1
                vz1 -= 1
            else: 
                vz1 +=  1
                vz0 -= 1
            
            update_vel_m0 = Velocity(vx = vx0, vy = vy0, vz = vz0)
            update_vel_m1 = Velocity(vx = vx1, vy = vy1, vz = vz1)

            moons[m0] = Moon(position= moon0.position, 
                            velocity = update_vel_m0)
            moons[m1] = Moon(position= moon1.position, 
                            velocity = update_vel_m1)
        # apply velocity
        for m0 in moons.keys():
            moon0 = moons[m0]
            vx0, vy0 , vz0 = moon0.velocity
            x0, y0, z0 = moon0.position
            update_pos_m0 = Position(x = x0 + vx0, y = y0 + vy0, z = z0 + vz0)
            moons[m0] = Moon(position= update_pos_m0, 
                            velocity = moon0.velocity)
        steps += 1
    return moons

def total_energy(moons: Dict[str,Moon]) -> int:
    values = moons.values()
    total = 0
    for pos,vel in values:
        moon_pot = sum(abs(val) for val in pos)
        moon_kin = sum(abs(val) for val in vel)
        total += (moon_pot * moon_kin)
    return total

TEST1="""<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

TEST = problem_prep(patt, TEST1)
assert total_energy(run_epochs(TEST, num_epochs=10)) == 179

TEST2 ="""<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""

TEST = problem_prep(patt, TEST2)
assert total_energy(run_epochs(TEST, num_epochs=100)) == 1940

# Part2

def run_epochs2(moons: Dict[str,Moon]) -> Dict[str, Moon]:
    
    seen_x = set()
    seen_y = set()
    seen_z = set()
    steps = 0
    done_x = done_y = done_z = False

    while True:
        moon_pairs = itertools.combinations(moons.keys(), 2)
        for m0,m1 in moon_pairs:
            moon0 = moons[m0]
            moon1 = moons[m1]
            vx0, vy0 , vz0 = moon0.velocity
            vx1, vy1 , vz1 = moon1.velocity
            x0, y0, z0 = moon0.position
            x1, y1, z1 = moon1.position
            
            #apply gravity
            if x0 == x1:
                pass
            elif x0 < x1:
                vx0 +=  1
                vx1 -= 1
            else: 
                vx1 +=  1
                vx0 -= 1

            if y0 == y1:
                pass
            elif y0 < y1:
                vy0 +=  1
                vy1 -= 1
            else: 
                vy1 +=  1
                vy0 -= 1
            
            if z0 == z1:
                pass
            elif z0 < z1:
                vz0 +=  1
                vz1 -= 1
            else: 
                vz1 +=  1
                vz0 -= 1
            
            update_vel_m0 = Velocity(vx = vx0, vy = vy0, vz = vz0)
            update_vel_m1 = Velocity(vx = vx1, vy = vy1, vz = vz1)

            moons[m0] = Moon(position= moon0.position, 
                            velocity = update_vel_m0)
            moons[m1] = Moon(position= moon1.position, 
                            velocity = update_vel_m1)
        # apply velocity
        for m0 in moons.keys():
            moon0 = moons[m0]
            vx0, vy0 , vz0 = moon0.velocity
            x0, y0, z0 = moon0.position
            update_pos_m0 = Position(x = x0 + vx0, y = y0 + vy0, z = z0 + vz0)
            moons[m0] = Moon(position= update_pos_m0, 
                            velocity = moon0.velocity)
        
        # part 2 checked JG solution based on lcm
        state_x, state_y, state_z = [], [], []

        for moon in moons.values():
            vx, vy, vz = moon.velocity
            x, y, z = moon.position
            curr_x = [x,vx]
            curr_y = [y,vy]                   
            curr_z = [z, vz]
            state_x.extend(curr_x)
            state_y.extend(curr_y)
            state_z.extend(curr_z)
        
        state_x, state_y, state_z= tuple(state_x), tuple(state_y), tuple(state_z)
        
        if not done_x and state_x in seen_x:
            total_x = steps
            done_x = True
            #print('total_x is', total_x)
        elif not done_x:
            seen_x.add(state_x)
        
        if not done_y and state_y in seen_y:
            total_y = steps
            done_y = True
            #print('total_y is', total_y)
        elif not done_y:
            seen_y.add(state_y)

        if not done_z and state_z in seen_z:
            total_z = steps
            done_z = True
            #print('total_z is', total_z)
        elif not done_z:
            seen_z.add(state_z)
        
        if all([done_x,done_y,done_z]):
            return total_x, total_y, total_z
        steps += 1
        

def number_steps(steps: Tuple[int,int,int]) -> int:
    """
    based on JG video solution; each cycle is assumed to be 
    smaller then total cycle (assumption as it could be bigger)
    and least common multiple of the 3 number is the solution
    """
    a, b, c = steps
    ab = (a * b) // math.gcd(a,b)
    ac = (ab * c) // math.gcd(ab,c)
    return ac

TEST = problem_prep(patt, TEST1)
assert number_steps(run_epochs2(TEST)) == 2772 

TEST2 = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""

TEST = problem_prep(patt, TEST2)
assert number_steps(run_epochs2(TEST)) == 4686774924

PUZZLE_INPUT="""<x=19, y=-10, z=7>
<x=1, y=2, z=-3>
<x=14, y=-4, z=1>
<x=8, y=7, z=-6>"""


if __name__ == "__main__":
    puzzle= problem_prep(patt, PUZZLE_INPUT)
    print("part1 total energy", total_energy(run_epochs(puzzle, num_epochs=1000)))
    print("part2 num of steps", number_steps(run_epochs2(puzzle)))
    



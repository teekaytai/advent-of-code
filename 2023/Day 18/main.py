# Credit goes to the users on the Advent of Code subreddit for this simple solution
# using the Shoelace formula and Pick's Theorem
import sys
from typing import NamedTuple

DIRECTIONS = 'RDLU'
MOVES: list[complex] = [1, -1j, -1, 1j]

class Instruction(NamedTuple):
    dz: complex
    dist: int

def parse_instruction_part1(inst: str) -> Instruction:
    direction, dist, _ = inst.split()
    dz = MOVES[DIRECTIONS.index(direction)]
    return Instruction(dz, int(dist))

def parse_instruction_part2(inst: str) -> Instruction:
    inst = inst.strip()
    dir_idx = int(inst[-2])
    dz = MOVES[dir_idx]
    dist = int(inst[-7:-2], 16)
    return Instruction(dz, dist)


area = 0
boundary_points = 0
prev = 0j
curr = 0j
for line in sys.stdin:
    # inst = parse_instruction_part1(line)
    inst = parse_instruction_part2(line)
    prev, curr = curr, curr + inst.dz * inst.dist
    # Use Shoelace formula to compute area
    area += int(prev.imag + curr.imag) * int(prev.real - curr.real)
    boundary_points += inst.dist
area = abs(area // 2)

# Use Pick's Theorem to find the number of points inside or on the boundary of the trench
# A = i + b/2 - 1  =>  i + b = A + b/2 + 1
print(area + boundary_points//2 + 1)

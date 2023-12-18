# A naive solution using flood fill, not fast enough to solve part 2.
# Could potentially be modified to compress the coordinates so that the time complexity
# is dependent only on number of points and not the actual magnitudes of the coordinates.
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


trench: set[complex] = set()
curr = 0j
for line in sys.stdin:
    inst = parse_instruction_part1(line)
    for _ in range(inst.dist):
        curr += inst.dz
        trench.add(curr)

stack = [1 - 1j]  # Identify a point inside the trench by manual inspection
while stack:
    z = stack.pop()
    for dz in MOVES:
        Z = z + dz
        if Z not in trench:
            trench.add(Z)
            stack.append(Z)
print(len(trench))

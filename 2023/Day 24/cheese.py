# According to the reddit solution megathread, it seems everyone's input will have a
# pair of hailstones with identical starting coordinates and velocities along one dimension.
# This would mean the rock we throw in part 2 must have this same start coordinate and
# velocity in that dimension, making it easy to solve for the remaining unknowns
import re
import sys
from typing import NamedTuple

Vector3D = tuple[int, int, int]

class Path3D(NamedTuple):
    start: Vector3D
    velocity: Vector3D


hailstones: list[Path3D] = []
for line in sys.stdin:
    values = tuple(map(int, re.findall(r'-?\d+', line)))
    hailstones.append(Path3D(values[:3], values[3:]))

k = -1
rock_start = [0] * 3
rock_velocity = [0] * 3
for i in range(3):
    seen: set[tuple[int, int]] = set()
    for p, v in hailstones:
        pair = p[i], v[i]
        if pair in seen:
            k = i
            rock_start[i] = p[i]
            rock_velocity[i] = v[i]
            break
        seen.add(pair)
    if rock_velocity[i] != 0:
        break
assert k >= 0

p1, v1 = hailstones[0]
p2, v2 = hailstones[1]
assert v1[k] != rock_velocity[k]
assert v2[k] != rock_velocity[k]
t1 = (p1[k] - rock_start[k]) // (rock_velocity[k] - v1[k])
t2 = (p2[k] - rock_start[k]) // (rock_velocity[k] - v2[k])
for i in range(3):
    if i == k:
        continue
    q1 = p1[i] + v1[i] * t1
    q2 = p2[i] + v2[i] * t2
    rock_velocity[i] = (q2 - q1) // (t2 - t1)
    rock_start[i] = q1 - rock_velocity[i] * t1

print(sum(rock_start))

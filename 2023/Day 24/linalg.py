# Alternative solution using Numpy to solve systems of linear equations to find intersections
from itertools import combinations
import numpy as np
import re
import sys
from typing import NamedTuple, Optional

# Set to 7 and 27 respectively for sample input
MIN_VAL = 200000000000000
MAX_VAL = 400000000000000

Vector = tuple[float, ...]
Vector2D = tuple[float, float]
Vector3D = tuple[float, float, float]

class Path(NamedTuple):
    start: Vector
    velocity: Vector

class Path2D(Path):
    start: Vector2D
    velocity: Vector2D

class Path3D(Path):
    start: Vector3D
    velocity: Vector3D

    def to_2d(self) -> Path2D:
        return Path2D(self.start[:2], self.velocity[:2])

def find_intersection(path1: Path, path2: Path) -> Optional[tuple[Vector, float, float]]:
    dimensions = len(path1.start)
    assert len(path2.start) == dimensions

    # Solve a system of 2 equations to find the times when each path reaches the intersection point
    coeffs = [
        [path1.velocity[0], -path2.velocity[0]],
        [path1.velocity[1], -path2.velocity[1]]
    ]
    constants = [
        path2.start[0] - path1.start[0],
        path2.start[1] - path1.start[1]
    ]
    try:
        t1, t2 = np.linalg.solve(coeffs, constants).round()
    except np.linalg.LinAlgError:
        return None
    # Ignore intersections in the past
    if t1 < 0 or t2 < 0:
        return None
    intersection = [path1.start[0] + path1.velocity[0]*t1, path1.start[1] + path1.velocity[1]*t1]
    # Check remaining dimensions intersect at same times
    for i in range(2, dimensions):
        z1 = path1.start[i] + path1.velocity[i] * t1
        z2 = path2.start[i] + path2.velocity[i] * t2
        if not np.isclose(z1, z2):
            return None
        intersection.append(z1)
    return tuple(intersection), t1, t2


hailstones: list[Path3D] = []
for line in sys.stdin:
    values = tuple(map(int, re.findall(r'-?\d+', line)))
    hailstones.append(Path3D(values[:3], values[3:]))

# Part 1
total = 0
for hailstone1, hailstone2 in combinations(hailstones, 2):
    result = find_intersection(hailstone1.to_2d(), hailstone2.to_2d())
    if result is None:
        continue
    intersection_x, intersection_y = result[0]
    if MIN_VAL <= intersection_x <= MAX_VAL and MIN_VAL <= intersection_y <= MAX_VAL:
        total += 1
print(total)

# Part 2
# Let the rock have starting position P = (X, Y, Z) and velocity V = (VX, VY, VZ).
# Let the i-th hailstone have starting position pi = (xi, yi, zi) and velocity vi = (vxi, vyi, vzi).
# Let the time the i-th hailstone gets hit be ti
# P + V * ti = pi + vi * ti
# => ti = (xi - X) / (VX - vxi) = (yi - Y) / (VY - vyi)
# => xi*VY - xi*vyi - X*VY + X*vyi = yi*VX - yi*vxi - Y*VX + Y*vxi
# => X*VY - Y*VX = X*vyi - Y*vxi - yi*VX + xi*VY - xi*vyi + yi*vxi
# => X*vyi - Y*vxi - yi*VX + xi*VY - xi*vyi + yi*vxi = X*vyj - Y*vxj - yj*VX + xj*VY - xj*vyj + yj*vxj
# => (vyi - vyj)*X + (vxj - vxi)*Y + (yj - yi)*VX + (xi - xj)*VY = xi*vyi - yi*vxi - xj*vyj + yj*vxj
# Solve for P and V using a system of 6 equations similar to the one above
coeffs: list[list[float]] = []
constants: list[float] = []
for (p1, v1), (p2, v2) in (hailstones[0], hailstones[1]), (hailstones[0], hailstones[2]):
    for i, j in combinations(range(3), 2):
        row = [0.] * 6
        row[i] = v1[j] - v2[j]
        row[j] = v2[i] - v1[i]
        row[3+i] = p2[j] - p1[j]
        row[3+j] = p1[i] - p2[i]
        coeffs.append(row)
        constants.append(p1[i]*v1[j] - p1[j]*v1[i] - p2[i]*v2[j] + p2[j]*v2[i])
# So much easier when you don't need to code the math yourself
solution = np.linalg.solve(coeffs, constants)
rock = Path3D(tuple(solution[:3]), tuple(solution[3:]))
for hailstone in hailstones:
    result = find_intersection(rock, hailstone)
    assert result is not None and result[1] == result[2]
print(round(sum(rock.start)))

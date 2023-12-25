from itertools import combinations, islice, product
import re
import sys
from typing import NamedTuple, Optional

# Set to 7 and 27 respectively for sample input
MIN_VAL = 200000000000000
MAX_VAL = 400000000000000

Vector2D = tuple[float, float]
Vector3D = tuple[float, float, float]

class Path2D(NamedTuple):
    start: Vector2D
    velocity: Vector2D

class Path3D(NamedTuple):
    start: Vector3D
    velocity: Vector3D

    def to_2d(self) -> Path2D:
        return Path2D(self.start[:2], self.velocity[:2])

def find_intersection(path1: Path2D, path2: Path2D) -> Optional[tuple[Vector2D, float, float]]:
    (x1, y1), (vx1, vy1) = path1
    (x2, y2), (vx2, vy2) = path2
    if vx1 == 0 and vx2 == 0:
        return None
    if vx1 == 0:
        t2 = (x1 - x2) / vx2
        intersection_x = x1
        intersection_y = x2 + vx2*t2
        t1 = (intersection_y - y1) / vy1
    elif vx2 == 0:
        t1 = (x2 - x1) / vx1
        intersection_x = x2
        intersection_y = x1 + vx1*t1
        t2 = (intersection_y - y2) / vy2
    else:
        m1 = vy1 / vx1
        m2 = vy2 / vx2
        if m1 == m2:
            return None
        c1 = y1 - m1*x1
        c2 = y2 - m2*x2
        intersection_x = (c2 - c1) / (m1 - m2)
        intersection_y = m1*intersection_x + c1
        t1 = (intersection_x - x1) / vx1
        t2 = (intersection_x - x2) / vx2
    # Ignore intersections in the past
    if t1 < 0 or t2 < 0:
        return None
    return (intersection_x, intersection_y), t1, t2

def intersects_point(path: Path3D, point: Vector3D) -> bool:
    (x, y, z), (vx, vy, vz) = path
    px, py, pz = point
    if vx != 0:
        t = (px - x) / vx
    elif vy != 0:
        t = (py - y) / vy
    else:
        t = (pz - z) / vz
    # Ignore intersections in the past
    if t < 0:
        return False
    return x + vx*t == px and y + vy*t == py and z + vz*t == pz


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
# Use brute force to find rock's velocity. For each attempt, subtract rock's velocity
# from each hailstone's velocity to get rock's frame of reference. Then, see if every
# hailstone intersects at a common point (which would be the stone's starting point)
(x1, y1, z1), (vx1, vy1, vz1) = hailstones[0]
(x2, y2, z2), (vx2, vy2, vz2) = hailstones[1]
for rock_vx, rock_vy in product(range(-1000, 1001), repeat=2):
    net_vx1 = vx1 - rock_vx
    net_vy1 = vy1 - rock_vy
    net_vx2 = vx2 - rock_vx
    net_vy2 = vy2 - rock_vy
    if net_vx1 == net_vy1 == 0 or net_vx2 == net_vy2 == 0:
        continue

    result = find_intersection(
        Path2D((x1, y1), (net_vx1, net_vy1)),
        Path2D((x2, y2), (net_vx2, net_vy2))
    )
    if result is None:
        continue
    (intersection_x, intersection_y), t1, t2 = result
    rock_vz = ((z2 + vz2*t2) - (z1 + vz1*t1)) / (t2 - t1)
    intersection_z = z1 + (vz1 - rock_vz)*t1
    rock_velocity = (rock_vx, rock_vy, rock_vz)
    intersection = (intersection_x, intersection_y, intersection_z)

    all_intersects = True
    for hailstone in islice(hailstones, 2, len(hailstones)):
        net_velocity = tuple(hail_v - rock_v for hail_v, rock_v in zip(hailstone.velocity, rock_velocity))
        if not intersects_point(Path3D(hailstone.start, net_velocity), intersection):
            all_intersects = False
            break
    if all_intersects:
        print(int(sum(intersection)))
        break

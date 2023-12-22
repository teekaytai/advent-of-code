from functools import reduce
from operator import attrgetter
import sys
from typing import NamedTuple

GROUND_HEIGHT = 0

class Brick(NamedTuple):
    lo_x: int
    hi_x: int
    lo_y: int
    hi_y: int
    lo_z: int
    hi_z: int

bricks: list[Brick] = []
max_x = 0
max_y = 0
for line in sys.stdin:
    endpoint1, endpoint2 = line.split('~')
    x1, y1, z1 = map(int, endpoint1.split(','))
    x2, y2, z2 = map(int, endpoint2.split(','))
    brick = Brick(*sorted((x1, x2)), *sorted((y1, y2)), *sorted((z1, z2)))
    bricks.append(brick)
    max_x = max(max_x, brick.hi_x)
    max_y = max(max_y, brick.hi_y)
N = len(bricks)
bricks.sort(key=attrgetter('lo_z'))

removable = [True] * N
# Stores sets of critical supports of each brick i - the bricks which if any one were removed
# would cause brick i to fall
crticial_supports: list[set[int]] = []
# This solution takes advantage of the very small range of the x- and y- coordinates (0-9).
# Keep track of the height and top-most bricks at each position
heights = [[GROUND_HEIGHT] * (max_x + 1) for _ in range(max_y + 1)]
brick_ids = [[-1] * (max_x + 1) for _ in range(max_y + 1)]
for i, brick in enumerate(bricks):
    lo_x, hi_x, lo_y, hi_y, lo_z, hi_z = brick
    tallest = GROUND_HEIGHT
    support_ids: set[int] = set()
    for y in range(lo_y, hi_y + 1):
        for x in range(lo_x, hi_x + 1):
            height = heights[y][x]
            if height > tallest:
                tallest = height
                support_ids = {brick_ids[y][x]}
            elif height == tallest and height > GROUND_HEIGHT:
                support_ids.add(brick_ids[y][x])

    new_height = tallest + hi_z - lo_z + 1
    for y in range(lo_y, hi_y + 1):
        for x in range(lo_x, hi_x + 1):
            heights[y][x] = new_height
            brick_ids[y][x] = i

    # Part 1
    if len(support_ids) == 1:
        support_id = next(iter(support_ids))
        removable[support_id] = False

    # Part 2
    if support_ids:
        cs = reduce(set.intersection, (crticial_supports[j] | {j} for j in support_ids))
        crticial_supports.append(cs)
    else:
        crticial_supports.append(set())

# Part 1
print(sum(removable))

# Part 2
print(sum(map(len, crticial_supports)))

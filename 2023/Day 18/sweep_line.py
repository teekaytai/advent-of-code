# Forgetting the shoelace formula we were taught in school, this solution was what I resorted to.
# The idea is to sweep a horizontal line from the bottom to the top of the trench.
# As the sweep line moves upwards, we maintain a list of intervals where a part of the trench
# intersects the sweep line. This will allow us to total up all the points in the trench
import sys
from typing import NamedTuple, Optional

DIRECTIONS = 'RDLU'
MOVES: list[int] = [(1, 0), (0, -1), (-1, 0), (0, 1)]

class Instruction(NamedTuple):
    dx: int
    dy: int
    dist: int

class Point(NamedTuple):
    x: int
    y: int

class HorizLine(NamedTuple):
    y: int
    lo_x: int
    hi_x: int

def parse_instruction_part1(inst: str) -> Instruction:
    direction, dist, _ = inst.split()
    dx, dy = MOVES[DIRECTIONS.index(direction)]
    return Instruction(dx, dy, int(dist))

def parse_instruction_part2(inst: str) -> Instruction:
    inst = inst.strip()
    dir_idx = int(inst[-2])
    dx, dy = MOVES[dir_idx]
    dist = int(inst[-7:-2], 16)
    return Instruction(dx, dy, dist)


# List of horizontal line segments from boundary of trench
h_lines: list[HorizLine] = []
prev = Point(0, 0)
curr = Point(0, 0)
for line in sys.stdin:
    # inst = parse_instruction_part1(line)
    inst = parse_instruction_part2(line)
    prev = curr
    curr = Point(curr.x + inst.dx * inst.dist, curr.y + inst.dy * inst.dist)
    if inst.dy == 0:
        h_lines.append(HorizLine(curr.y, min(prev.x, curr.x), max(prev.x, curr.x)))
# Sort line segments in order of y-coordinate, the order in which the sweep line will encounter them
h_lines.sort()

# List of intervals where there is currently trench at the sweep line
intervals: list[list[int, int]] = []
# Start sweep line at lowest y-coordinate
curr_y = h_lines[0].y
total_points = 0
for h_line in h_lines:
    y, lo_x, hi_x = h_line
    if y > curr_y:
        # Sweep line has moved upwards, add points swept to total_points
        total_width = sum(right_x - left_x + 1 for left_x, right_x in intervals)
        total_points += (y - curr_y) * total_width
        curr_y = y

    # Look for intervals that intersect with h_line
    left_intersect_interval: Optional[list[int, int]] = None
    right_intersect_interval: Optional[list[int, int]] = None
    middle_intersect_interval: Optional[list[int, int]] = None
    for interval in intervals:
        left_x, right_x = interval
        if left_x == lo_x or left_x == hi_x:
            left_intersect_interval = interval
        if right_x == lo_x or right_x == hi_x:
            right_intersect_interval = interval
        if left_x < lo_x and right_x > hi_x:
            middle_intersect_interval = interval

    if middle_intersect_interval:
        # One section of trench splits into 2 disjoint intervals
        intervals.append([hi_x, middle_intersect_interval[1]])
        middle_intersect_interval[1] = lo_x
    elif left_intersect_interval is None and right_intersect_interval is None:
        # h_line is the start of a new disjoint section of trench
        intervals.append([lo_x, hi_x])
        total_points += hi_x - lo_x + 1
    elif left_intersect_interval is None:
        # An interval's right endpoint is moved
        if right_intersect_interval[1] == hi_x:
            right_intersect_interval[1] = lo_x
        else:
            right_intersect_interval[1] = hi_x
            total_points += hi_x - lo_x
    elif right_intersect_interval is None:
        # An interval's left endpoint is moved
        if left_intersect_interval[0] == lo_x:
            left_intersect_interval[0] = hi_x
        else:
            left_intersect_interval[0] = lo_x
            total_points += hi_x - lo_x
    elif left_intersect_interval is right_intersect_interval:
        # One interval exactly matches h_line, meaning this line marks the end of a section of trench
        intervals.remove(left_intersect_interval)
    else:
        # Two intervals merge together into a single bigger interval
        left_intersect_interval[0] = right_intersect_interval[0]
        intervals.remove(right_intersect_interval)
        total_points += hi_x - lo_x - 1

print(total_points)

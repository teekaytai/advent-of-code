
import sys
from typing import Iterator

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
PIPE_ADJS = {
    '|': [(-1, 0), (1, 0)],
    '-': [(0, 1), (0, -1)],
    'L': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    '7': [(1, 0), (0, -1)],
    'F': [(0, 1), (1, 0)],
    '.': []
}

def pipe_neighbours(grid: list[list[str]], r: int, c: int) -> Iterator[tuple[int, int]]:
    pipe = grid[r][c]
    for dr, dc in PIPE_ADJS[pipe]:
        yield r + dr, c + dc

grid = [list(line.strip()) for line in sys.stdin]
H = len(grid)
W = len(grid[0])
start_row, start_col = next((r, c) for r, row in enumerate(grid) for c, cell in enumerate(row) if cell == 'S')

# Replace start cell 'S' with correct pipe
start_adjs = set()
for dr, dc in DIRS:
    adj_r = start_row + dr
    adj_c = start_col + dc
    if 0 <= adj_r < H and 0 <= adj_c < W and (start_row, start_col) in pipe_neighbours(grid, adj_r, adj_c):
        start_adjs.add((dr, dc))
grid[start_row][start_col] = next(pipe for pipe, adjs in PIPE_ADJS.items() if set(adjs) == start_adjs)

# Part 1
# Use DFS to trace out pipe loop, then calculate the distance to the farthest position based on the loop's length
loop_cells: list[tuple[int, int]] = []
prev = (-1, -1)
curr = (start_row, start_col)
while not loop_cells or curr != loop_cells[0]:
    loop_cells.append(curr)
    for adj in pipe_neighbours(grid, *curr):
        if adj != prev:
            prev, curr = curr, adj
            break
print(len(loop_cells) // 2)

# Part 2
# Compute area enclosed using shoelace formula
area = sum((prev[1] + curr[1]) * (prev[0] - curr[0]) for prev, curr in zip(loop_cells, loop_cells[1:]))
area += (loop_cells[-1][1] + loop_cells[0][1]) * (loop_cells[-1][0] - loop_cells[0][0])
area = abs(area // 2)
# Find number of interior points using Pick's Theorem:
# A = i + b/2 - 1  =>  i = A - b/2 + 1
print(area - len(loop_cells) // 2 + 1)

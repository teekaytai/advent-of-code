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
is_loop_part = [[False] * W for _ in range(H)]
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
# BFS to trace out pipe loop
is_loop_part[start_row][start_col] = True
queue = [(start_row, start_col)]
next_queue: list[tuple[int, int]] = []
steps = 0
while queue:
    for r, c in queue:
        for adj_r, adj_c in pipe_neighbours(grid, r, c):
            assert 0 <= adj_r < H and 0 <= adj_c < W
            if not is_loop_part[adj_r][adj_c]:
                is_loop_part[adj_r][adj_c] = True
                next_queue.append((adj_r, adj_c))
    queue = next_queue
    next_queue = []
    steps += 1
print(steps - 1)

# Part 2
# Iterate over rows of the grid and keep track of whether we are inside or outside the loop.
# We flip sides when we cross over '|', 'L---7' or 'F---J'. 'L---J' and 'F---7' do not flip.
total_enclosed = 0
for r in range(H):
    c = 0
    is_inside = False
    while c < W:
        if not is_loop_part[r][c]:
            total_enclosed += is_inside
        elif grid[r][c] == '|':
            is_inside = not is_inside
        else:
            loop_enter_top = grid[r][c] == 'L'
            c += 1
            while grid[r][c] == '-':
                c += 1
            loop_exit_top = grid[r][c] == 'J'
            if loop_enter_top ^ loop_exit_top:
                is_inside = not is_inside
        c += 1
print(total_enclosed)

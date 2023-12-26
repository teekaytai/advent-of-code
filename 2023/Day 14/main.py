import sys

LEGEND = '.#O'
EMPTY_SPACE = 0
CUBE_ROCK = 1
ROUND_ROCK = 2
K = len(LEGEND)

NUM_SPIN_CYCLES = 1_000_000_000

def compute_load(grid: list[list[int]]) -> int:
    return sum(row.count(ROUND_ROCK) * i for i, row in enumerate(reversed(grid), start=1))

def tilt_north(grid: list[list[int]]) -> list[list[int]]:
    top_empty_pos = [0] * len(grid[0])
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == CUBE_ROCK:
                top_empty_pos[c] = r + 1
            elif cell == ROUND_ROCK:
                row[c] = EMPTY_SPACE
                grid[top_empty_pos[c]][c] = ROUND_ROCK
                top_empty_pos[c] += 1
    return grid

def rotate_cw(grid: list[list[int]]) -> list[list[int]]:
    return [list(reversed(col)) for col in zip(*grid)]


grid = [[LEGEND.index(char) for char in line.strip()] for line in sys.stdin]

# Part 1
print(compute_load(tilt_north(grid)))

# Part 2
# Map grids to the step number it was seen at
grid_history: dict[tuple[tuple[int, ...]], int] = {}
steps_left = NUM_SPIN_CYCLES
while steps_left:
    # Make grid immutable for hashing
    frozen_grid = tuple(map(tuple, grid))
    prev_seen_step = grid_history.get(frozen_grid, -1)
    if prev_seen_step > 0:
        cycle_len = prev_seen_step - steps_left
        steps_left %= cycle_len
    else:
        grid_history[frozen_grid] = steps_left

    for _ in range(4):
        grid = rotate_cw(tilt_north(grid))
    steps_left -= 1
print(compute_load(grid))

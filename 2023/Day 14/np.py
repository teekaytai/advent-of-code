from nptyping import NDArray, Shape
import numpy as np
import sys

LEGEND = '.#O'
EMPTY_SPACE = 0
CUBE_ROCK = 1
ROUND_ROCK = 2
K = len(LEGEND)

NUM_SPIN_CYCLES = 1_000_000_000

IntArray2D = NDArray[Shape['*, *'], np.int_]

def compute_load(grid: IntArray2D) -> np.int_:
    return np.sum((grid == ROUND_ROCK).sum(axis=1) * np.arange(grid.shape[0], 0, -1))

def tilt_north(grid: IntArray2D) -> IntArray2D:
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

def rotate_cw(grid: IntArray2D) -> IntArray2D:
    return np.rot90(grid, axes=(1, 0))

# Losslessly compress a matrix of ints into a single int for use in hashing
def compress(grid: IntArray2D) -> np.int_:
    return np.sum(grid.ravel() * np.cumprod(np.full_like(grid, K)))


grid = np.array([[LEGEND.index(char) for char in line.strip()] for line in sys.stdin])

# Part 1
print(compute_load(tilt_north(grid)))

# Part 2
# Map grids to the step number it was seen at
grid_history: dict[np.int_, int] = {}
steps_left = NUM_SPIN_CYCLES
while steps_left:
    compressed_grid = compress(grid)
    prev_seen_step = grid_history.get(compressed_grid, -1)
    if prev_seen_step > 0:
        cycle_len = prev_seen_step - steps_left
        steps_left %= cycle_len
    else:
        grid_history[compressed_grid] = steps_left

    for _ in range(4):
        grid = rotate_cw(tilt_north(grid))
    steps_left -= 1
print(compute_load(grid))

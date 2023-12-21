import sys

ROCK = '#'
DIRS: list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]

grid = [line.strip() for line in sys.stdin]
N = len(grid)
M = N // 2

def bfs(start_r: int, start_c: int) -> list[int]:
    counts = [1]
    even_cells = {(start_r, start_c)}
    odd_cells: set[tuple[int, int]] = set()
    queue = [(start_r, start_c)]
    next_queue: list[tuple[int, int]] = []
    i = 0
    while queue:
        i += 1
        for r, c in queue:
            for dr, dc in DIRS:
                R = r + dr
                C = c + dc
                p = (R, C)
                if R < 0 or R >= N or C < 0 or C >= N or grid[R][C] == ROCK:
                    continue
                if i % 2 == 1:
                    if p not in odd_cells:
                        odd_cells.add(p)
                        next_queue.append(p)
                else:
                    if p not in even_cells:
                        even_cells.add(p)
                        next_queue.append(p)
        counts.append(len(odd_cells) if i % 2 == 1 else len(even_cells))
        queue = next_queue
        next_queue = []
    return counts


counts = bfs(M, M)  # Start is in centre cell

# Part 1

print(counts[64])

# Part 2

# Observations/Asumptions
# - Grid is 131x131, and 26501365 = 202300 * 131 + 65
# - The start cell is right in the middle of the grid
# - There are no rocks in the middle row or column, or along the border, allowing the Elf to reach other grids
#   in a minimal number of steps without detouring around rocks
# - There is a diamond shape connecting the centres of the borders that has no rocks
# - Rocks are generally sparse. Together with the above, the grid is clear enough such that starting from the
#   centre, any cell within 26501365 taxicab distance (that is not completely surrounded by rocks) can also
#   be reached within 26501365 actual steps

# The reachable area will be a diamond, fully containing some grids but slicing into the corners of the outermost
# grids. The calculation has to take into account the different parities of grids and the corners to add/remove

K = 26501365
L = K // N
odd_total_count = counts[-2]
even_total_count = counts[-1]
odd_corners_count = odd_total_count - counts[65]
even_corners_count = even_total_count - counts[64]
print((L+1)**2 * odd_total_count + L**2 * even_total_count - (L+1) * odd_corners_count + L * even_corners_count)

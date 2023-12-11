import sys

EMPTY_SPACE = '.'
EXPANSION_SIZE = 1000000  # Set to 2 for part 1

def man_dist(point1: tuple[int, int], point2: tuple[int, int]) -> int:
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

image = [line.strip() for line in sys.stdin]

# Map old coordinates to new coordinates in expanded universe
row_mapping = []
curr_row = 0
for row in image:
    row_mapping.append(curr_row)
    curr_row += EXPANSION_SIZE if all(cell == EMPTY_SPACE for cell in row) else 1
col_mapping = []
curr_col = 0
for col in zip(*image):
    col_mapping.append(curr_col)
    curr_col += EXPANSION_SIZE if all(cell == EMPTY_SPACE for cell in col) else 1

galaxies = [
    (row_mapping[r], col_mapping[c])
    for r, row in enumerate(image)
    for c, cell in enumerate(row)
    if cell != EMPTY_SPACE
]
total_dist = sum(
    man_dist(galaxy1, galaxies[j])
    for i, galaxy1 in enumerate(galaxies)
    for j in range(i)
)
print(total_dist)

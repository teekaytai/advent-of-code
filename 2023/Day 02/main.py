import math
import sys

# For part 1
CUBE_LIMITS = {'red': 12, 'green': 13, 'blue': 14}

total_part1 = 0
total_part2 = 0
for line in sys.stdin:
    game_label, records = line.split(': ')
    game_id = int(game_label.split()[1])
    cube_counts = {'red': 0, 'green': 0, 'blue': 0}
    for record in records.strip().split('; '):
        for cube_count in record.split(', '):
            count_str, colour = cube_count.split()
            cube_counts[colour] = max(cube_counts[colour], int(count_str))

    if all(count <= CUBE_LIMITS[colour] for colour, count in cube_counts.items()):
        total_part1 += game_id

    total_part2 += math.prod(cube_counts.values())

print(total_part1)
print(total_part2)

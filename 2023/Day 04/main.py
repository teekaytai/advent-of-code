import sys

lines = [*sys.stdin]
total_points = 0
card_counts = [1] * len(lines)

for i, line in enumerate(lines):
    lst = line.split()
    divider_idx = lst.index('|')
    winning_numbers = set(lst[2:divider_idx])
    elf_numbers = set(lst[divider_idx+1:])
    num_matches = len(winning_numbers & elf_numbers)

    total_points += 2 ** (num_matches - 1) if num_matches else 0

    for j in range(i + 1, i + 1 + num_matches):
        card_counts[j] += card_counts[i]

print(total_points)
print(sum(card_counts))

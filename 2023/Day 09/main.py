import sys

total = 0
for line in sys.stdin:
    # Part 1
    # diffs = [int(x) for x in line.split()]
    # Part 2
    diffs = [int(x) for x in reversed(line.split())]
    next_term = 0
    while any(num != 0 for num in diffs):
        next_term += diffs[-1]
        diffs = [y - x for x, y in zip(diffs, diffs[1:])]
    total += next_term
print(total)

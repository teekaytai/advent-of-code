import sys

def is_symbol(char: str) -> bool:
    return not (char.isdigit() or char == '.')

schematic = [list(line.strip()) for line in sys.stdin]
H = len(schematic)
W = len(schematic[0])
gear_numbers = [[[] for _ in range(W)] for _ in range(H)]

total = 0
for r, row in enumerate(schematic):
    lo = 0
    while lo < W:
        if not row[lo].isdigit():
            lo += 1
            continue

        hi = lo + 1
        while hi < W and row[hi].isdigit():
            hi += 1
        num = int(''.join(row[lo:hi]))

        is_part_num = False
        for R in range(r - 1, r + 2):
            if R < 0 or R >= H:
                continue
            for C in range(lo - 1, hi + 1):
                if C < 0 or C >= W or not is_symbol(schematic[R][C]):
                    continue
                is_part_num = True
                if schematic[R][C] == '*':
                    gear_numbers[R][C].append(num)
        if is_part_num:
            total += num

        lo = hi + 1

print(total)
print(sum(lst[0] * lst[1] for row in gear_numbers for lst in row if len(lst) == 2))

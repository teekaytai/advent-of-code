MOD = 256

def holiday_hash(chars: str) -> int:
    h = 0
    for char in chars:
        h = (h + ord(char)) * 17 % MOD
    return h


operations = input().split(',')

# Part 1
print(sum(map(holiday_hash, operations)))

# Part 2
lenses: dict[str, int] = {}
for op in operations:
    if op[-1] == '-':
        label = op[:-1]
        lenses.pop(label, None)
    else:
        label, focal_len = op.split('=')
        lenses[label] = int(focal_len)

# Rely on the lenses dict preserving its insertion order to ensure each box receives lenses in original order
boxes: list[list[int]] = [[] for _ in range(MOD)]
for label, focal_len in lenses.items():
    boxes[holiday_hash(label)].append(focal_len)
print(sum(
    i * sum(j * focal_len for j, focal_len in enumerate(box, start=1))
    for i, box in enumerate(boxes, start=1)
))

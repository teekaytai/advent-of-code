from collections import deque
import sys

items = deque(int(x) for x in input().split()[1:])
new_items: list[int] = []

for line in sys.stdin:
    if not line[0].isdigit():
        items += new_items
        new_items.clear()
        continue
    dst_start, src_start, size = map(int, line.split())
    for _ in range(len(items)):
        item = items.popleft()
        if src_start <= item < src_start + size:
            new_items.append(item - src_start + dst_start)
        else:
            items.append(item)

items += new_items
print(min(items))

from collections import deque
from operator import itemgetter
import sys

seed_ranges = [int(x) for x in input().split()[1:]]
# Convert (start, size) pairs to half-open intervals [start, start + size)
item_intervals = deque((start, start + size) for start, size in zip(seed_ranges[::2], seed_ranges[1::2]))
new_item_intervals: list[tuple[int, int]] = []

for line in sys.stdin:
    if not line[0].isdigit():
        item_intervals += new_item_intervals
        new_item_intervals.clear()
        continue
    dst_start, src_start, size = map(int, line.split())
    src_end = src_start + size
    for _ in range(len(item_intervals)):
        item_start, item_end = item_intervals.popleft()
        if item_end > src_start and item_start < src_end:
            overlap_start = max(item_start, src_start)
            overlap_end = min(item_end, src_end)
            new_item_intervals.append((overlap_start - src_start + dst_start, overlap_end - src_start + dst_start))
            if item_start < src_start:
                item_intervals.append((item_start, src_start))
            if item_end > src_end:
                item_intervals.append((src_end, item_end))
        else:
            item_intervals.append((item_start, item_end))

item_intervals += new_item_intervals
print(min(map(itemgetter(0), item_intervals)))

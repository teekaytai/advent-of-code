from collections import deque
from operator import itemgetter
import sys

seed_ranges = [int(x) for x in input().split()[1:]]
item_intervals = deque((seed_ranges[i], seed_ranges[i] + seed_ranges[i + 1]) for i in range(0, len(seed_ranges), 2))
new_item_intervals: list[tuple[int, int]] = []

for line in sys.stdin:
    if not line[0].isdigit():
        item_intervals += new_item_intervals
        new_item_intervals.clear()
        continue
    dst_start, src_start, size = map(int, line.split())
    src_end = src_start + size
    for _ in range(len(item_intervals)):
        item_lo, item_hi = item_intervals.popleft()
        if item_hi >= src_start and item_lo <= src_end:
            overlap_lo = max(item_lo, src_start)
            overlap_hi = min(item_hi, src_end)
            new_item_intervals.append((overlap_lo - src_start + dst_start, overlap_hi - src_start + dst_start))
            if item_lo < src_start:
                item_intervals.append((item_lo, src_start - 1))
            if item_hi > src_end:
                item_intervals.append((src_end + 1, item_hi))
        else:
            item_intervals.append((item_lo, item_hi))

item_intervals += new_item_intervals
print(min(map(itemgetter(0), item_intervals)))

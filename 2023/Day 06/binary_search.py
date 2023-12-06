from typing import Callable

def binary_search(test: Callable[[int], bool], lo: int, hi: int) -> bool:
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if test(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

# Part 1
# times = [int(x) for x in input().split()[1:]]
# distances = [int(x) for x in input().split()[1:]]

# Part 2
times = [int(''.join(input().split()[1:]))]
distances = [int(''.join(input().split()[1:]))]

product = 1
for time, dist in zip(times, distances):
    def dist_travelled(button_time: int) -> int:
        return (time - button_time) * button_time

    def beats_record(button_time: int) -> bool:
        return dist_travelled(button_time) > dist

    # Find button hold time that maximises distance travelled using peak finding.
    # Alternatively, it can be computed directly as time/2 since this value maximises (time - x) * x.
    peak = binary_search(lambda x: dist_travelled(x) >= dist_travelled(x + 1), 1, time - 1)
    min_button_time = binary_search(beats_record, 1, peak)
    max_button_time = binary_search(lambda x: not beats_record(x), peak + 1, time)
    product *= max_button_time - min_button_time
print(product)

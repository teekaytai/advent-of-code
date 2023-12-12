from functools import cache
import sys

OPERATIONAL = '.'
DAMAGED = '#'
UNKNOWN = '?'

UNFOLD_SIZE = 5

total = 0
for line in sys.stdin:
    springs, nums = line.split()
    groups = [int(x) for x in nums.split(',')]

    # "Unfold" inputs for part 2
    springs = UNKNOWN.join([springs] * UNFOLD_SIZE)
    groups *= UNFOLD_SIZE

    N = len(springs)
    M = len(groups)

    # Precompute longest possible runs of damaged (or unknown) springs starting at each index.
    # Not necessary for program to finish quickly, but does improve time complexity to be
    # independent of group sizes.
    longest_damaged_runs = [0] * N
    longest_damaged_runs[-1] = 1 if springs[-1] != OPERATIONAL else 0
    for i in range(N - 2, -1, -1):
        longest_damaged_runs[i] = 1 + longest_damaged_runs[i + 1] if springs[i] != OPERATIONAL else 0
    last_damaged_idx = springs.rfind(DAMAGED)

    # dp(i, j) returns the number of possible assignments that make
    # springs[i:N] correspond to groups[j:M]
    @cache
    def dp(i: int, j: int) -> int:
        if j == M:
            return 1 if i > last_damaged_idx else 0
        if i >= N:
            return 0

        num_ways = 0
        # Case where i-th spring is operational, so form groups with remaining springs
        if springs[i] != DAMAGED:
            num_ways += dp(i + 1, j)
        # Case where i-th spring is damaged, so ensure first groups[j] springs are damaged or unknown,
        # and that the (i + groups[j])-th spring is operational (or the group ends at the last spring)
        if springs[i] != OPERATIONAL:
            group_end_idx = i + groups[j]
            if longest_damaged_runs[i] >= groups[j] and (
                group_end_idx == N or springs[group_end_idx] != DAMAGED
            ):
                num_ways += dp(group_end_idx + 1, j + 1)
        return num_ways

    total += dp(0, 0)

print(total)

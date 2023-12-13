import sys
from typing import Callable

# For part 2
NUM_DIFFERENCES = 1

# int.bit_count method introduced in Python 3.10
bit_count: Callable[[int], int] = (
    int.bit_count if hasattr(int, 'bit_count') else lambda num: bin(num).count('1')
)

# Encode each sequence as a bitmask to quickly check for equality
def encode_seq(seq: str) -> int:
    return int(seq.replace('.', '0').replace('#', '1'), 2)

def find_palindrome_centre(nums: list[int]) -> int:
    N = len(nums)
    for centre in range(1, N):
        # Part 1
        # Alternatively, part 2's code can handle part 1 by setting NUM_DIFFERENCES to 0
        # if all(nums[centre - i - 1] == nums[centre + i] for i in range(min(centre, N - centre))):
        #     return centre

        # Part 2
        total_differences = 0
        for i in range(min(centre, N - centre)):
            total_differences += bit_count(nums[centre - i - 1] ^ nums[centre + i])
            if total_differences > NUM_DIFFERENCES:
                break
        if total_differences == NUM_DIFFERENCES:
            return centre
    return 0

total = 0
patterns = sys.stdin.read().split('\n\n')
for pattern in patterns:
    grid = pattern.split()
    encoded_rows = [encode_seq(row) for row in grid]
    encoded_cols = [encode_seq(''.join(cols)) for cols in zip(*grid)]
    total += find_palindrome_centre(encoded_cols) or 100 * find_palindrome_centre(encoded_rows)
print(total)

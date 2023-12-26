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

# For part 1, Manacher's algorithm can be used to achieve a linear time complexity for finding palindromes.
# For part 2, we can get a head start finding elements that match, but revert back to checking each pair
# and counting up differences after the first difference is found
def find_palindrome_centre(nums: list[int]) -> int:
    # Add dummy numbers (-1) between elements so only odd length palindromes
    # need to be considered and simplify algorithm
    N = len(nums) * 2 - 1
    expanded_nums = [-1] * N
    expanded_nums[::2] = nums
    palindrome_radii: list[int] = []
    # Boundaries of outer palindrome
    lo = -1
    hi = -1
    for centre in range(N):
        radius = 0
        if centre <= hi:
            mirror_centre = lo + (hi - centre)
            radius = min(hi - centre, palindrome_radii[mirror_centre])
        l = centre - radius - 1
        r = centre + radius + 1
        while l >= 0 and r < N and expanded_nums[l] == expanded_nums[r]:
            radius += 1
            l -= 1
            r += 1
        if centre + radius > hi:
            lo = centre - radius
            hi = centre + radius
        palindrome_radii.append(radius)

        # Part 1
        # Check if palindrome is centred on dummy element, representing an even-length palindrome
        # in the original sequence, and if the palindrome spans until one end of the sequence
        # if centre % 2 == 1 and (l == -1 or r == N):
        #     return (centre + 1) // 2

        # Part 2
        # Check if palindrome is centred on dummy element, then continue expanding palindrome as
        # long as not too many different bits found
        if centre % 2 == 0:
            continue
        total_differences = 0
        while l >= 0 and r < N:
            total_differences += bit_count(expanded_nums[l] ^ expanded_nums[r])
            if total_differences > NUM_DIFFERENCES:
                break
            l -= 1
            r += 1
        if total_differences == NUM_DIFFERENCES:
            return (centre + 1) // 2
    return 0

total = 0
patterns = sys.stdin.read().split('\n\n')
for pattern in patterns:
    grid = pattern.split()
    encoded_rows = [encode_seq(row) for row in grid]
    encoded_cols = [encode_seq(''.join(cols)) for cols in zip(*grid)]
    total += find_palindrome_centre(encoded_cols) or 100 * find_palindrome_centre(encoded_rows)
print(total)

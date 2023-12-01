# Solution using Rabin-Karp with multiple patterns for O(km + qn) expected time complexity, where
# k is the number of patterns to find,
# m is the length of each pattern hashed,
# q is the number of lines to search through, and
# n is the average length of a line

import sys
from typing import Optional

D = 26  # Number of english letters

def rabin_hash(pattern: str) -> int:
    h = 0
    for letter in pattern:
        h = h * D + ord(letter) - ord('a')
    return h

def roll_hash(h: int, letter: str, pat_len: str) -> int:
    return (h * D + ord(letter) - ord('a')) % D**pat_len

NUM_NAMES = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
MIN_NAME_LEN = min(map(len, NUM_NAMES))  # Only hash this many characters from back of each pattern
PATTERN_HASHES = {rabin_hash(name[-MIN_NAME_LEN:]): num for num, name in enumerate(NUM_NAMES, start=1)}

total = 0
collisions = 0
for line in sys.stdin:
    left_num = -1
    right_num = -1
    h = 0
    for i, char in enumerate(line):
        num_found: Optional[int] = None
        if char.isdigit():
            num_found = int(char)
            h = 0
        else:
            h = roll_hash(h, char, MIN_NAME_LEN)
            num = PATTERN_HASHES.get(h, None)
            if num is None:
                continue
            name = NUM_NAMES[num - 1]
            if line[i-len(name)+1:i+1] == name:
                num_found = num
            else:
                collisions += 1
        if num_found is not None:
            if left_num < 0:
                left_num = num_found
            right_num = num_found
    total += 10 * left_num + right_num
print(total)
print('Number of hash collisions:', collisions)  # I got 15 collisions over 1000 lines

# If the last numbers in the history are e, d, c, b, and a, then the differences work out as follows:
# [e, d, c, b, a]
# [d-e, c-d, b-c, a-b]
# [c-2d+e, b-2c+d, a-2b+c]
# [b-3c+3d-e, a-3b+3c-d]
# [a-4b+6c-4d+e]
# We see the coefficients alternate in signs and have coefficients following rows of Pascal's triangle.
# To get the next term in the sequence, we need to sum the last terms in each difference array.
# For each unknown, we can sum up the coefficients using the hockey stick identity
# (also known as the Christmas stocking identity :D).

from math import comb
import sys

total = 0
for line in sys.stdin:
    # Part 1
    # nums = [int(x) for x in reversed(line.split())]
    # Part 2
    nums = [int(x) for x in line.split()]
    total += sum((-1)**i * x*comb(len(nums), i+1) for i, x in enumerate(nums))
print(total)
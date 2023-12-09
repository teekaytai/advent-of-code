import numpy as np
from numpy.polynomial.polynomial import polyfit, polyval
import sys

# The process described in the preamble is the Method of Finite Differences,
# which is used to calculate values of a polynomial.
# We can obtain a good estimate of the final answer by finding the polynomial directly
# and evaluating it to find the next and previous terms.
total_part1 = 0
total_part2 = 0
for line in sys.stdin:
    nums = [int(y) for y in line.split()]
    N = len(nums)
    coefs = polyfit(x=np.arange(N), y=nums, deg=N-1)
    total_part1 += round(polyval(N, coefs))
    total_part2 += round(polyval(-1, coefs))
print(total_part1)
print(total_part2)

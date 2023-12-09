# The process described in the preamble is the Method of Finite Differences,
# which is used to calculate values of a polynomial.
# We can obtain a good estimate of the final answer by approximating the polynomials directly
# and evaluating them to find the next and previous terms of each history.

import numpy as np
from numpy.polynomial.polynomial import polyfit, polyval
import sys

ys = np.array([[int(y) for y in line.split()] for line in sys.stdin]).T
N = ys.shape[0]
coefs = polyfit(x=np.arange(N), y=ys, deg=N-1)
print(polyval(N, coefs).round().sum(dtype=int))  # Part 1
print(polyval(-1, coefs).round().sum(dtype=int))  # Part 2

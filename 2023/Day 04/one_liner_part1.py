from collections import Counter
from math import prod
import sys

print(sum(prod(Counter(line.split()).values()) // 2 for line in sys.stdin))
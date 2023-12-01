import sys

INF = 10000000
NUM_NAMES = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

def find(text: str, pattern: str) -> int:
    idx = text.find(pattern)
    return idx if idx >= 0 else INF

def rfind(text: str, pattern: str) -> int:
    idx = text.rfind(pattern)
    return idx if idx >= 0 else -INF

total = 0
for line in sys.stdin:
    min_idx = INF
    left_num = -1
    max_idx = -INF
    right_num = -1
    for num, num_name in enumerate(NUM_NAMES, start=1):
        lo_idx = min(find(line, str(num)), find(line, num_name))
        hi_idx = max(rfind(line, str(num)), rfind(line, num_name))
        if lo_idx < min_idx:
            min_idx = lo_idx
            left_num = num
        if hi_idx > max_idx:
            max_idx = hi_idx
            right_num = num
    total += 10 * left_num + right_num
print(total)

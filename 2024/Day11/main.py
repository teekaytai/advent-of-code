from functools import cache

a = [int(x) for x in input().split()]

@cache
def f(x, i):
    if i == 0:
        return 1
    elif x == 0:
        return f(1, i - 1)
    elif len(s := str(x)) % 2 == 0:
        return f(int(s[:len(s)//2]), i - 1) + f(int(s[len(s)//2:]), i - 1)
    else:
        return f(x*2024, i - 1)

print(sum(f(x, 25) for x in a))
print(sum(f(x, 75) for x in a))

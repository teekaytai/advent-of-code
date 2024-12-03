import re
a = 1
t1 = 0
t2 = 0
for m in re.finditer(r'do\(\)|don\'t\(\)|mul\((\d+),(\d+)\)',open(0).read()):
    if m[0] == 'do()': a = 1
    elif m[0] == 'don\'t()': a = 0
    else:
        t1+=int(m[1]) * int(m[2])
        t2+=a*int(m[1]) * int(m[2])
print(t1)
print(t2)

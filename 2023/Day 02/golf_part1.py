import re
i=0
print(sum((i:=i+1)*all(int(n)<13+(c<'r')+(c<'g')for n,c in re.findall('(\d+) (.)',l))for l in open(0)))
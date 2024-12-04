from itertools import product
import re

s = open(0).read()
n = s.find('\n')
print(sum(
    len(re.findall(f'(?={gap.join(xmas)})', s, re.DOTALL))
    for xmas, gap in product(['XMAS', 'SAMX'], ['', f'.{{{n-1}}}', f'.{{{n}}}', f'.{{{n+1}}}'])))
print(len(
    re.findall('|'.join(f'(?={tl}.{tr}.{{{n-1}}}A.{{{n-1}}}{bl}.{br})'
                        for (tl, br), (tr, bl) in product(('MS', 'SM'), repeat=2)),
               s, re.DOTALL)))

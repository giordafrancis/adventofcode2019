"""
G. Smith      2.2 - 1.6     1.0 - 1.5     33 - 55     660
F. John       1.4 - 0.2.                  60          850 (early) - 1100 (late)
R. Kahn       1.9 - 1.4     1.9                       700 - 850
L. Terry      0.6 - 0.35.   1.8.          60          1100 - 1400
"""
import re

test = "R. Kahn       1.9 - 1.4     1.9                       700 - 850"
row = re.split("\s{3,}", test)
last_col = re.split("\s{2,}", test)[-1] # eg '850 (early) - 1100 (late)' or '600'
patt = re.compile("(?P<num1>[0-9]+)[a-zA-z(\)\- ]+(?P<num2>[0-9]+)")
g = patt.search(last_col)

if g:
    val = (int(g.group('num1')) + int(g.group('num2'))) / 2
else:
    val = int(last_col)

print(val, row)



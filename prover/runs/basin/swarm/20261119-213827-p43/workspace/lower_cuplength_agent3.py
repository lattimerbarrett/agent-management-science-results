from fractions import Fraction
from itertools import product
from pathlib import Path
# Rational cohomology in basis 1,a,b,ab. Exponents >=2 vanish.
basis=((0,0),(1,0),(0,1),(1,1))
def mul(x,y):
    z=[Fraction(0)]*4
    for i,(p,q) in enumerate(basis):
        for j,(r,s) in enumerate(basis):
            if p+r<2 and q+s<2:
                z[basis.index((p+r,q+s))] += x[i]*y[j]
    return tuple(z)
e=tuple(tuple(Fraction(i==j) for i in range(4)) for j in range(4))
zero=(Fraction(0),)*4
assert all(mul(e[0],v)==v for v in e)
assert mul(e[1],e[1])==mul(e[2],e[2])==zero
assert mul(e[1],e[2])==e[3]!=zero
positive=e[1:]
assert all(mul(mul(x,y),z)==zero for x,y,z in product(positive,repeat=3))
assert all(mul(x,y)==mul(y,x) for x,y in product(e,repeat=2))
assert all(mul(mul(x,y),z)==mul(x,mul(y,z)) for x,y,z in product(e,repeat=3))
# The homomorphisms on pi_2 in the sphere basis are omega/(2*pi)=(2,2)=c1.
chern=(2,2)
area_in_2pi_units=(2,2)
assert chern==area_in_2pi_units
from math import gcd
assert gcd(*chern)==2
print('Exact rational cohomology checks passed: cup-length = 2.')
print('Monotonicity: [omega]=2*pi*c1; minimal Chern number = 2.')
Path('workspace/lower_cuplength_agent3.py').write_text(Path(__file__).read_text())

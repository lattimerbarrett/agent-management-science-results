from fractions import Fraction as F

def states(x):
    x1,x2,x3=x
    return ((x1+x2+x3)/3,(x1+x2)/2,(x2+x3)/2)
def q(x):
    return sorted(states(x))[1]
a=(F(0),F(2),F(1,2))
b=(F(0),F(2),F(3,4))
c=tuple(y-x for x,y in zip(a,b))
assert all(x>=0 for x in c) and any(x>0 for x in c)
assert q(a)==q(b)==1
assert q(c)==F(1,12)>0
# Every nonzero vector in the positive octant has at least two strictly
# positive state values: verify this support property on all nonempty supports.
from itertools import product
for support in product((0,1), repeat=3):
    if not any(support): continue
    values=states(tuple(F(x) for x in support))
    assert sum(v>0 for v in values)>=2
# A symbolic exact check of the upper-bound certificate:
# eta<=u and eta<=1-u -> 1-2eta=(u-eta)+(1-u-eta)>=0.
import sympy as s
eta,u=s.symbols('eta u', real=True)
assert s.expand((u-eta)+(1-u-eta)-(1-2*eta))==0
print('Faithful monotone median counterexample:', states(a),states(b),q(a),q(b),q(c))
print('Upper-bound certificate identity checked exactly.')

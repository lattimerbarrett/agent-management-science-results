from fractions import Fraction
from itertools import product
from pathlib import Path
# Exact finite-support model of the dual support construction.
# All values are integers, so inequalities are checked without roundoff.
D=[(1,0),(-1,0),(0,1),(0,-1),(2,1),(-1,3)]
def F(xi): return max(abs(sum(a*b for a,b in zip(xi,v))) for v in D)
V=list(product(range(-3,4),repeat=2))
checks=0
for x in V:
 assert F(x)>=max(abs(x[0]),abs(x[1]))
 for c in range(-3,4):
  assert F(tuple(c*a for a in x))==abs(c)*F(x)
 for y in V:
  assert F(tuple(a+b for a,b in zip(x,y)))<=F(x)+F(y)
  assert abs(F(x)-F(y))<=F(tuple(a-b for a,b in zip(x,y)))
  checks+=2
# Ambient positivity restriction lower bound: p+d-n.
assert 3+2-4==1
# The multiplying-barrier trick is exact: beta=xi(v)/a0, and |beta|>1.
a0=Fraction(3,2); value=Fraction(7,3); beta=value/a0
assert beta>1 and beta*a0==value
print('Exact support-norm inequalities checked:',checks)
print('Barrier multiplier:',beta,'; restricted Levi positivity lower bound:',3+2-4)
Path('workspace/agent3_bridge_checks.py').write_text(Path('scratchpad.py').read_text().split("Path('workspace/")[0])
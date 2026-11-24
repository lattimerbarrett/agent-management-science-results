import sympy as s
from fractions import Fraction as F
from pathlib import Path
C,t,v=s.symbols('C t v', positive=True)
# Interior regimes, where all arguments are >=1.
D=lambda x:1-1/x
assert s.simplify(D(C/t)+D(C/(2-t))-2*D(C))==0
slack=s.factor(D(C/(1-v))-D(C)*(2-D((C-1)/v**2)))
assert s.simplify(slack-v*(1-v)/C)==0
# Boundary regimes: C/(2-t)<1 gives slack (2-t-C)/C >=0.
assert s.simplify(D(C/t)-2*D(C)-(2-t-C)/C)==0
# (C-1)/v^2<1 gives slack (1+v-C)/C; C<1+v^2<1+v.
assert s.simplify(D(C/(1-v))-2*D(C)-(1+v-C)/C)==0
def d(x): return max(F(0),1-1/x)
count=0
for den in range(2,22):
 for cc in range(den,8*den):
  c=F(cc,den)
  for j in range(1,den):
   z=F(j,den)
   assert d(c/z)+d(c/(2-z))>=2*d(c)
   assert d(c/(1-z))>=d(c)*(2-d((c-1)/z**2)) if c>1 else True
   count+=1
print('Exact symbolic regime identities and',count,'rational functional checks passed.')

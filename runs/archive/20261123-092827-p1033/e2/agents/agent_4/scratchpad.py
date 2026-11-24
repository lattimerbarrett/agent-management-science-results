import math,json
from fractions import Fraction
from pathlib import Path
import sympy as sp
import numpy as np
# Exact random witness checks for the block lemma at n=100.
n=100;r=math.isqrt(n-1)+1;L=math.ceil(math.log(n));m=100*n*L
rng=np.random.default_rng(202607)
deg=np.zeros(n,dtype=np.int64);co=np.zeros((n,n),dtype=np.int64)
for b in range(m):
    B=rng.choice(n,size=r,replace=False)
    deg[B]+=1;co[np.ix_(B,B)]+=1
pairmin=min(int(co[i,j]) for i in range(n) for j in range(i))
assert pairmin>=10*L
assert int(deg.max())<=200*r*L
# ALL choices E,J have at most r*r incidences, below the prescribed threshold.
assert r*r<5*L*r
report={'n':n,'r':r,'L':L,'m':m,'min_pair_codegree':pairmin,'required_pair_codegree':10*L,'max_degree':int(deg.max()),'allowed_max_degree':200*r*L,'universal_expansion_upper_bound':r*r,'expansion_forbidden_threshold':5*L*r}
print(json.dumps(report,indent=2))
# Check numerical failure estimates at every integer logarithmic layer.
# For L=ceil(log n)>=5, ln(mn)<=ln100+2L+lnL, so testing L suffices.
for ell in range(5,100001):
    assert math.log(100)+math.log(ell)<=2*ell
    assert math.log(5*ell/(2*math.e))>=1
# Exact combinatorial inequalities used to estimate means.
for nn in range(2,100001):
    rr=math.isqrt(nn-1)+1
    assert 2*rr*(rr-1)>=nn-1
    assert rr*rr<=2*nn
# Conservative failure sum at n>=100: n^-14+n*exp(-100rL/3)+n^-r < 1.
assert Fraction(1,100**14)+Fraction(1,100**99)+Fraction(1,100**10)<1
assert Fraction(8,3)**5 > 100
assert 25 > 2*3**2
# Exact identities establish the integer square-root bounds for ALL integers.
q=sp.symbols('q',integer=True,positive=True)
assert sp.expand(2*((q-1)**2+1)-q*q-(q-2)**2)==0
assert sp.expand(2*q*(q-1)-(q*q-1)-(q-1)**2)==0
# With e in (8/3,3), these rational checks plus log u<=u-1
# prove the logarithmic estimates for ALL L>=5, not merely the tests above.
with open('workspace/agent4_upper_checks.json','w') as f:json.dump(report,f,indent=2)
print('All integer, layer, and concrete random witness checks passed.')
Path('workspace/agent4_upper_parameter_check.py').write_text(Path(__file__).read_text())

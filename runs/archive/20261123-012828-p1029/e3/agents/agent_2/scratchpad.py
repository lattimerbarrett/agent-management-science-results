"""Exact checks for established implications, not for unproved AW* existence."""
from fractions import Fraction
from pathlib import Path
import json
import sympy as sp

# Universal polynomial certificate for the two-increment upper bound.
e,u,v = sp.symbols('eta u v', real=True)
assert sp.expand((u-e)+(1-u-e) - (1-2*e)) == 0

# Rational telescoping obstruction: q=k*p+r, 0<=r<p, eta=p/q.
p,k,r = sp.symbols('p k r', integer=True)
q=k*p+r
assert sp.expand((k+1)*p-q) == p-r
# Thus N=k+1 gives N*eta>1 whenever p>0, 0<=r<p.

# Exact extensive rational checks, including endpoints and arbitrary large N.
checks=[]
for den in range(1,301):
    for num in range(1,den+1):
        eta=Fraction(num,den)
        N=den//num+1
        assert N*eta>1
        assert Fraction(0)<=eta<=Fraction(1)
        checks.append((num,den,N))

# Scaling preserves order constraints as an algebraic identity:
# t=eta_new/eta>0; difference t*(a_next-a)= t*a_next-t*a.
t,a,b=sp.symbols('t a b',commutative=False)
assert sp.expand(t*(b-a)-(t*b-t*a))==0

result={
 'rational_telescoping_cases':len(checks),
 'largest_chosen_N':max(c[2] for c in checks),
 'upper_certificate':'(u-eta)+(1-u-eta)=1-2*eta',
 'telescoping_certificate':'(k+1)*p-(k*p+r)=p-r>0 when 0<=r<p',
 'scope':'Checks algebraic certificates only; no lower-bound construction is asserted.'}
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent2_exact_checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))

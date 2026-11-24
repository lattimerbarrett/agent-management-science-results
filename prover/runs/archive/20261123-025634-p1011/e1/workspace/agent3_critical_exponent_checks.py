import sympy as s
from pathlib import Path
n=s.symbols('n',integer=True,positive=True)
q=2*n/(n-2);p=(n+2)/(n-2);qp=2*n/(n+2)
assert s.simplify(p*qp-q)==0
assert s.simplify(1/qp-p/q)==0
assert s.simplify(2/n+2/q-1)==0
assert s.simplify((p-1)*n/2-q)==0
# At n19, positive-part f' has Holder exponent alpha=4/17.
alpha=s.Rational(4,17);x=s.symbols('x',positive=True)
assert s.diff(x**alpha,x,2).is_negative
assert s.simplify((1+alpha)*s.integrate(s.Symbol('t',positive=True)**alpha,(s.Symbol('t',positive=True),0,1)))==1
# Gram perturbation positivity can be checked dimension-free by operator norm:
# ||G^{-1}E||<1 implies invertibility via Neumann series; no numerical matrix used.
print('PASS: exact critical Holder/Sobolev exponents, concavity f-prime, integrated Taylor constant.')

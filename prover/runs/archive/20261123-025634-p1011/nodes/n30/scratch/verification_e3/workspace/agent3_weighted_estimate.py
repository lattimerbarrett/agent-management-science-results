"""Exact exponent checks for the weighted integral estimate.

For any fixed positive first Robin eigenfunction phi normalized by integral phi=1,
Green's identity for a positive solution gives
  n(n-2) integral(phi*u**p) = lambda1 integral(phi*u),
where p=(n+2)/(n-2). Jensen implies
  integral(phi*u) <= (lambda1/(n(n-2)))**((n-2)/4),
  integral(phi*u**p) <= (lambda1/(n(n-2)))**((n+2)/4).
This is NOT a compactness estimate: p is below the Sobolev critical exponent.
"""
import sympy as s
n=s.symbols("n",positive=True,integer=True)
p=(n+2)/(n-2)
assert s.simplify(1/(p-1)-(n-2)/4)==0
assert s.simplify(p/(p-1)-(n+2)/4)==0
assert s.simplify(2*n/(n-2)-p-1)==0
print("Weighted integral estimate exponents checked; no compactness asserted.")

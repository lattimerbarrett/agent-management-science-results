"""Exact verification of the all-red-loop upper-bound calculation."""
import sympy as s
r,t=s.symbols("r t", positive=True)
a=t*t
f=(1-(3+a)*r+3*r*r)/(1-r)
assert s.simplify(s.diff(f,r)-(-2-a+6*r-3*r*r)/(1-r)**2)==0
assert s.simplify(f.subs(r,t)-(1-t)**2)==0
# The derivative numerator increases for r<1, hence r<=t<=1/2 implies
# numerator <= -2+t*6-4*t*t = -2*(1-t)*(1-2*t)<=0.
assert s.expand(-2+6*t-4*t*t+2*(1-t)*(1-2*t))==0
print("all-red-loop Goodman certificate: exact identities passed")

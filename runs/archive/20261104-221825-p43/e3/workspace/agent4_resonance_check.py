"""Exact symbolic identity underpinning monotonicity of the resonance E."""
import sympy as s
x,P,u=s.symbols("x P u", positive=True)
Z=1-P-x
f=(1-x)**2/Z
assert s.simplify(s.diff(f,x)+1-P**2/Z**2)==0
D=x+f*u*u
assert s.simplify(s.diff(D,x)-(1-u*u+u*u*P**2/Z**2))==0
print("Resonance denominator derivative identity checked exactly.")

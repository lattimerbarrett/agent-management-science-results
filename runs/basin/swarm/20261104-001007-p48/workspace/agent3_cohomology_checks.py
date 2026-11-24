import sympy as s
from pathlib import Path
e,t=s.symbols('e t', nonnegative=True, integer=True)
C2=80*e+32; c2=65*e+26; CK=-20*e-16
# Verify K.C directly: K=(-2,-e-2), C=(4,12e+4).
CKdirect=s.expand(-e*(-2)*4+(-2)*(12*e+4)+(-e-2)*4)
assert CKdirect==CK
chi=s.factor((t+1)-CK*t*(t+1)/4+C2*t*(t+1)*(2*t+1)/12-c2*t*(t+1)*(t+2)/6)
assert s.expand(chi.subs(t,1))==-15*e
assert s.factor(chi.subs(e,0))==(t-1)**2*(t+1)
# h1(O(5S-f)) is sum h1(P1,O(-1-ke)), k=0,...,5.
assert sum(range(6))*e==15*e
print('χ(Sym^t E)=',chi)
print('h*(E0)=(0,15e,0), checked π-pushforward summands O(-1-ke), k=0,...,5.')

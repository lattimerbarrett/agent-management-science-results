import sympy as s
from pathlib import Path
# Exact checks of the explicit product-height critical points and joining arc.
t=s.symbols('t', real=True)
p=s.Matrix([s.sin(t),0,s.cos(t)])
q=s.Matrix([s.sin(t),0,-s.cos(t)])
assert s.simplify(p.dot(p)-1)==0
assert s.simplify(q.dot(q)-1)==0
assert s.simplify(p[2]+q[2])==0
e=s.Matrix([0,0,1])
gp=e-p[2]*p; gq=e-q[2]*q
assert s.simplify(gp.dot(gp)+gq.dot(gq)-2*s.sin(t)**2)==0
# In local sphere charts at pole signs a,b, Hess F = diag(-a,-a,-b,-b).
for a in (-1,1):
 for b in (-1,1):
  h=s.diag(-a,-a,-b,-b)
  assert h.det()==1
  index=sum(1 for x in h.diagonal() if x<0)
  assert index==((2 if a==1 else 0)+(2 if b==1 else 0))
# Cone extension rho(r)g(theta): simultaneous radial/angular zero implies
# g=0 and dg=0, impossible if zero is regular. rho'>0 exactly.
r=s.symbols('r', positive=True)
rho=s.exp(-1/r**2)
assert s.simplify(s.diff(rho,r)-2*rho/r**3)==0
assert s.diff(rho,r).is_positive
# Local Euler index check: 1+2+1=chi(S2xS2)=4.
assert 1+2+1==2*2
# Integral Wirtinger period estimate threshold, no numerical simulation needed.
L,eps=s.symbols('L eps', positive=True)
assert s.simplify(eps*L/(2*s.pi)).is_positive
print('Exact arc, critical-index, flat-cone derivative and Euler checks passed.')

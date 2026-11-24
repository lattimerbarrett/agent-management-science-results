import sympy as s
from pathlib import Path
aa,bb,cc=s.symbols('aa bb cc')
A=s.Matrix([[aa,bb],[bb,cc]])
x,y,u,v,B=s.symbols('x y u v B')
R=s.Matrix([x,y]);W=s.Matrix([u,v])
Rp=R+A*W
Bp=B+(R.T*W)[0]+s.Rational(1,2)*(W.T*A*W)[0]
S=B-s.Rational(1,2)*(R.T*A.inv()*R)[0]
Sp=Bp-s.Rational(1,2)*(Rp.T*A.inv()*Rp)[0]
assert s.factor(S-Sp)==0
# Explicit osculating sphere adapted bubble condition in signed curvature k.
k,e=s.symbols('k e',nonzero=True,real=True)
t=k*e**2/(1+s.sqrt(1-k**2*e**2))
assert s.simplify(2*t/k-t**2-e**2)==0
print('Forced Schur base-shift identity and osculating-sphere bubble identity checked.')
if __file__.endswith('scratchpad.py'):
 Path('workspace/agent1_forced_schur_checks.py').write_text(Path(__file__).read_text())

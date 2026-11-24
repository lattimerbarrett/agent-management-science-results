import sympy as s
from pathlib import Path

a=s.symbols('a', positive=True)
x,y,c=s.symbols('x y c',real=True)
b=x+s.I*y
C=2*((x*x+y*y+1)/a-c)
H=s.Matrix([[a,b],[s.conjugate(b),c+C/2]])
assert s.simplify(H.det())==1
T=s.simplify(s.trace(H))
eps=1/(2*T)
He=H-eps*s.eye(2)
assert s.simplify(He.det()-(s.Rational(1,2)+1/(4*T*T)))==0
assert s.simplify(a*T-(a*a+x*x+y*y+1))==0
# Hence H > 0 and H-eps I > 0 by principal-minor criterion.
print('Adjusted Hessian =',H)
print('det(adjusted Hessian) =',s.factor(H.det()))
print('trace =',T)
print('det(H - I/(2 trace H)) =',s.factor(He.det()))
print('All exact symbolic identities passed.')
Path('workspace/agent1_psh_check.py').write_text(Path(__file__).read_text())

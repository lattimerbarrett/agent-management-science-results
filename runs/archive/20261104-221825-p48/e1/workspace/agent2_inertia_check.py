import sympy as s
from pathlib import Path
a,c,g=s.symbols('a c gamma', positive=True)
b=s.symbols('b',complex=True)
u0,u1,u2=s.symbols('u0 u1 u2',complex=True)
K=s.Matrix([[a,b],[s.conjugate(b),c]])
D=s.zeros(4)
D[:2,:2]=K
D[2,2]=-g
u=s.Matrix([u0,u1,u2,1])
H=D+u*u.conjugate().T
T=s.eye(4)
for i,ui in enumerate([u0,u1,u2]):
    T[3,i]=-s.conjugate(ui)
congruence=s.simplify(T.conjugate().T*H*T)
expected=D.copy(); expected[3,3]=1
assert congruence==expected
assert s.simplify(H.det()+g*K.det())==0
assert T.det()==1
print('Exact symbolic congruence proves inertia(H)=(3 positive,1 negative) whenever K>0 and gamma>0.')
print('det H=',s.factor(H.det()))
Path('workspace/agent2_inertia_check.py').write_text(Path(__file__).read_text())

import sympy as s
from pathlib import Path
h1,h2,g=s.symbols('h1 h2 gamma',real=True, nonzero=True)
c1,c2=s.symbols('c1 c2',complex=True)
H=s.diag(h1,h2)
C=s.Matrix([c1,c2])
A=H.row_join(C).col_join(s.Matrix([[s.conjugate(c1),s.conjugate(c2),-g]]))
T=s.eye(3)
T[2,0]=s.conjugate(c1)/g
T[2,1]=s.conjugate(c2)/g
expected=s.zeros(3); expected[:2,:2]=H+C*C.conjugate().T/g;expected[2,2]=-g
assert s.simplify(T.conjugate().T*A*T-expected)==s.zeros(3)
# h1 > 0, h2 <0. Schur repaired positive iff determinant >0.
S=H+C*C.conjugate().T/g
assert s.simplify(S.det() - (h1*h2 +(h2*c1*s.conjugate(c1)+h1*c2*s.conjugate(c2))/g))==0
print('Exact Schur repair criterion: h1*h2 + (h2*|c1|^2+h1*|c2|^2)/gamma > 0.')
print('Small gamma only helps if h1*|c2|^2 > (-h2)*|c1|^2; merely nonzero bad-direction component is insufficient.')
Path('workspace/agent2_schur_repair_check.py').write_text(Path(__file__).read_text())

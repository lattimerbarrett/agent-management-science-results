import sympy as s
from pathlib import Path
# Execute independently supplied checks, rather than merely print assertions.
for fn in ['workspace/agent2_cohomology.py','workspace/agent3_finsler_levi.py','workspace/agent4_lower_bound.py']:
    p=Path(fn)
    print('\nRUN',fn)
    if p.exists():
        exec(compile(p.read_text(),fn,'exec'),{'__name__':'__main__'})
# Wirtinger derivatives treat barred variables as independent.
z1,z2,w1,w2,Z1,Z2,W1,W2=s.symbols('z1 z2 w1 w2 Z1 Z2 W1 W2')
a,d,b,c=s.symbols('a d b c',real=True)
z=[z1,z2,w1,w2]; zb=[Z1,Z2,W1,W2]
Q=a*z1*Z1+(b+s.I*c)*z1*Z2+(b-s.I*c)*z2*Z1+d*z2*Z2
G=s.exp(-Q)*(w1*W1+w2*W2)
psi=1/G
origin={z1:0,z2:0,Z1:0,Z2:0,w1:1,W1:1,w2:0,W2:0}
Levi=s.Matrix(4,4,lambda i,j:s.simplify(s.diff(psi,z[i],zb[j]).subs(origin)))
expected=s.Matrix([[a,b+s.I*c,0,0],[b-s.I*c,d,0,0],[0,0,1,0],[0,0,0,-1]])
assert Levi==expected
assert s.factor(expected[:2,:2].det())==a*d-b*b-c*c
assert s.factor(expected.det())==-(a*d-b*b-c*c)
print('Exact local Levi matrix:'); print(Levi)
print('All available checks and independent Levi computation passed.')

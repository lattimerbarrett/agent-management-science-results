import sympy as s
from pathlib import Path
r=s.symbols('r',positive=True,real=True)
# For s=||v||² at v=(r,0), Hessian s^{-1} on two complex fibre directions
vgrad=s.Matrix([r,0]); fibre=-s.eye(2)/r**4+2*(vgrad*vgrad.T)/r**6
assert fibre==s.diag(r**-4,-r**-4)
a,b,c,d=s.symbols('a b c d',real=True)
# Griffiths curvature in selected v direction is Hermitian [[a,c+id],[c-id,b]]
R=s.Matrix([[a,c+s.I*d],[c-s.I*d,b]])
H=s.diag(R/r**2,fibre)
assert s.simplify(H.det()+(a*b-c*c-d*d)/r**12)==0
# Cohomological codimensions for candidate generated ample rank-two bundles.
h=lambda a,b:(a+1)*(b+1)
assert h(3,3)-h(2,2)==7
assert h(0,3)==4
assert 7>3 and 4>2
e=s.symbols('e',integer=True,nonnegative=True)
def intersect(D,E):
    a,b=D; c,d=E
    return s.expand(-e*a*c+a*d+b*c)
A=(5,-1); B=(-1,12*e+5)
assert intersect(A,(1,e))==-1
assert intersect(B,(0,1))==-1
# A 3-positive form on C4 restricts with >=1 positive to every complex surface.
assert 3+2-4==1
code=Path('scratchpad.py').read_text()
Path('workspace/agent4_sign_checks.py').write_text(code)
print('Verified inverse-norm Levi fibre block:',fibre)
print('Verified full Levi determinant:',s.factor(H.det()))
print('Verified common-component codimensions 7>3 and 4>2.')

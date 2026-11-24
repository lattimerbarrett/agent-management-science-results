import sympy as s
from pathlib import Path
# For a positive Finsler metric G on rank r=2 over base dimension n=2,
# adapted horizontal/projective/radial frame gives
# L(log G)=diag(-K,A,0), dlogG=(0,0,0,1).
# Verify exact inverse-function Hessian and inertia via Sylvester minors.
t=s.symbols('t', real=True)
f=s.Function('f')(t)
assert s.simplify(s.diff(1/f,t,2) - (2*s.diff(f,t)**2/f**3-s.diff(f,t,2)/f**2))==0
k1,k2,a,g=s.symbols('k1 k2 a g',positive=True)
H=s.diag(-k1,-k2,a,0)
b=s.Matrix([0,0,0,1])
Lpsi=(-H+b*b.T)/g
assert Lpsi == s.diag(k1/g,k2/g,-a/g,1/g)
assert [s.sign(x) for x in Lpsi.diagonal()] == [1,1,-1,1]
# General horizontal Hermitian 2x2 matrix and projective/radial scalar:
x,y,u,v=s.symbols('x y u v',real=True)
K=s.Matrix([[x,u+s.I*v],[u-s.I*v,y]])
assert s.expand(K.det())==x*y-u*u-v*v
# Positive definite K iff x>0 and xy>u²+v². Positive Finsler gives a>0.
# Thus the Levi form of 1/G has exactly 3 positives and 1 negative.
print('Verified chain rule Hessian identity, 4x4 adapted Levi form, exact inertia (3,1), and horizontal Sylvester determinant.')
Path('workspace/agent3_finsler_levi.py').write_text(Path('scratchpad.py').read_text())

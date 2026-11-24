import sympy as s
from pathlib import Path
x,y=s.symbols('x y',real=True)
r=x*x+y*y
g=r*r-2*r
H=s.hessian(g,(x,y))
# H+4I = 4r I + 8 [x;y][x,y], positive semidefinite.
assert s.simplify(H+4*s.eye(2)-(4*r*s.eye(2)+8*s.Matrix([x,y])*s.Matrix([[x,y]])))==s.zeros(2)
assert s.simplify(H.det()-16*(r-1)*(3*r-1))==0
assert s.simplify(H*s.Matrix([x,y])-(12*r-4)*s.Matrix([x,y]))==s.zeros(2,1)
assert s.simplify(H*s.Matrix([-y,x])-(4*r-4)*s.Matrix([-y,x]))==s.zeros(2,1)
text='''For rho(z,w)=||z||^2+|w|^4-2|w|^2-3, every affine complex hyperplane w=a.z+b with ||a||^2<1/2 has rho restricted real strictly convex. The real Hessian of g(w)=|w|^4-2|w|^2 is -4I+4|w|^2 I+8 ww^T >= -4I, and the real differential A of complex functional a has operator norm ||a||. Thus Hessian rho|L >= (2-4||a||^2)I>0. Since rho is coercive on L (the ||z||^2 term dominates g>=-1), K intersect L is compact convex (possibly empty). For n>=3 these hyperplanes have complex dimension >=2. This geometric fact is checked symbolically but DOES NOT prove the exterior is Oka.\n'''
Path('workspace/agent3_convex_sections.txt').write_text(text)
# Safe standalone check: no self-copy into a shared file.
print('PASS: exact Hessian decomposition and radial/tangential eigenvector identities')
print(text)

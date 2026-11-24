import sympy as s
from pathlib import Path
e=s.symbols('e', nonnegative=True, integer=True)
def dot(D,F):
 a,b=D; c,d=F
 return s.expand(-e*a*c+a*d+b*c)
S=(1,0); f=(0,1); H=(1,3*e+1); P=(4,12*e+3)
A=(5,-1); B=(-1,12*e+5); C=(4,12*e+4)
assert s.simplify(dot(A,H)-(10*e+4))==0
assert s.simplify(dot(B,H)-(10*e+4))==0
assert s.simplify(dot(C,C)-(80*e+32))==0
assert s.simplify(dot(A,B)-(65*e+26))==0
assert s.simplify(dot(A,P)-(40*e+11))==0
assert s.simplify(dot(B,P)-(40*e+17))==0
assert s.simplify((dot(C,C)-dot(A,B))-(15*e+6))==0
# Exact eigenvalues of vertical Hessian of reciprocal norm on C^2.
z,t=s.symbols('z t', positive=True, real=True)
x1,y1,x2,y2=s.symbols('x1 y1 x2 y2', real=True)
fexpr=1/(x1*x1+y1*y1+x2*x2+y2*y2)
# complex Hessian at (z,0), all imaginary coordinates zero
coords=[(x1,y1),(x2,y2)]
M=s.zeros(2)
for a,(x,y) in enumerate(coords):
 for b,(u,v) in enumerate(coords):
  M[a,b]=s.simplify((s.diff(fexpr,x,u)+s.diff(fexpr,y,v)+s.I*s.diff(fexpr,x,v)-s.I*s.diff(fexpr,y,u))/4)
M=M.subs({x1:z,y1:0,x2:0,y2:0})
assert M==s.diag(z**-4,-z**-4)
print('Intersection identities verified symbolically for every e>=0.')
print('Reciprocal norm vertical complex Hessian:', M)
print('Thus a Griffiths-positive E gives 3 positive Levi directions (2 horizontal + radial); angular direction is negative.')
Path('workspace/agent2_verified.py').write_text(Path('scratchpad.py').read_text())

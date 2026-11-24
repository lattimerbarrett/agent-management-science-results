import sympy as s
import pathlib
Q1,Q2,P1,P2,A,B=s.symbols('Q1 Q2 P1 P2 A B',real=True)
r2=Q1**2+Q2**2
out=s.Matrix([2*P2+4*Q2/r2+2,2*P1+4*Q1/r2+2,1-Q2/2,1-Q1/2])
coords=s.Matrix([Q1,Q2,P1,P2]); D=out.jacobian(coords)
Om=s.Matrix([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])
assert s.simplify(D.T*Om*D-Om)==s.zeros(4)
S=-(Q1*B+Q2*A)/2+Q1+Q2+A+B+s.log(r2)
# Input momenta -S_Q and output momenta S_Qnew.
oldP=s.Matrix([-s.diff(S,Q1),-s.diff(S,Q2)])
newP=s.Matrix([s.diff(S,A),s.diff(S,B)])
assert s.simplify(out[:2,0].subs({P1:oldP[0],P2:oldP[1]})-s.Matrix([A,B]))==s.zeros(2,1)
assert newP==out[2:,0]
X1,X2,Y1,Y2=s.symbols('X1 X2 Y1 Y2')
linear=s.Matrix([X1+Y1,X2+Y2,(X2-Y2)/2,(Y1-X1)/2]).jacobian([X1,X2,Y1,Y2])
originalOm=s.Matrix([[0,1,0,0],[-1,0,0,0],[0,0,0,-1],[0,0,1,0]])
assert linear.T*Om*linear==originalOm
# Exact equal-area disk parameterization checked by area density.
u,v=s.symbols('u v',real=True); f=s.sqrt(1-(u*u+v*v)/4)
x=s.Matrix([u*f,v*f,1-(u*u+v*v)/2])
assert s.simplify(x.dot(x.diff(u).cross(x.diff(v))))==1
print('PASS: limit map symplectic; type1 generator exact; canonical linear change exact; sphere disk area density=1.')
print('Limit generator:',S)

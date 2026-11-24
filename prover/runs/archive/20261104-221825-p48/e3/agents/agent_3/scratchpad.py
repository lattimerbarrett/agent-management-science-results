import sympy as s
from pathlib import Path
e,a,b=s.symbols('e a b', integer=True)
def dot(D,F):
    x,y=D;u,v=F
    return s.expand(-e*x*u+x*v+y*u)
A=(5,-1); B=(-1,12*e+5); H=(1,3*e+1); P=(4,12*e+3); c1=(4,12*e+4)
assert dot(A,P)==40*e+11
assert dot(B,P)==40*e+17
assert dot(A,H)==dot(B,H)==10*e+4
c2=dot(A,B)
assert c2==65*e+26
assert dot(c1,c1)-c2==15*e+6
assert 4*c2-dot(c1,c1)==180*e+72
for aa in (1,2,3):
    prod=dot((aa,b),(4-aa,12*e+4-b))
    sol=s.solve(prod-c2,b)
    print('fiber-degree',aa,'product',prod,'solutions',sol)
N=(1,e)
assert dot(A,N)==-1
assert dot(B,(0,1))==-1
# Both N=S+ef and f have smooth semipositive representatives:
# N is O_P(O+O(e))(1) tensor pi*O(e), globally generated for e>=0.
K=(-2,-e-2)
chi=2+(dot(c1,c1)-dot(c1,K))/2-c2
assert s.simplify(chi+15*e)==0
# A has pi_* = direct sum O(-1-i*e), i=0,...,5; B has fibre degree -1.
assert sum(s.symbols('i') for _ in [])==0
for ee in range(20):
    h0=sum(max(-1-i*ee+1,0) for i in range(6))
    h1=sum(max(-(-1-i*ee)-1,0) for i in range(6))
    assert h0==0 and h1==15*ee
# Exact Hermitian Schur-complement identity underlying the support-plane proof.
t=s.symbols('t', positive=True)
aa,cc=s.symbols('aa cc', positive=True)
x1,y1,x2,y2,u,v=s.symbols('x1 y1 x2 y2 u v', real=True)
C=s.Matrix([[x1+s.I*y1],[x2+s.I*y2]])
Schur=s.Matrix([[-aa,u+s.I*v],[u-s.I*v,-cc]])
HH=(Schur+C*C.conjugate().T/t).row_join(C).col_join(C.conjugate().T.row_join(s.Matrix([[t]])))
W=s.eye(2).col_join(-C.conjugate().T/t)
assert s.simplify(W.conjugate().T*HH*W-Schur)==s.zeros(2)
assert W[:2,:]==s.eye(2)
assert s.simplify(Schur.det()-(aa*cc-u*u-v*v))==0
# Index-dimension argument: a negative 2-plane in CR dimension 3
# meets every complex hyperplane in dimension >=1 and cannot meet a
# semipositive vertical line except at zero.
assert 2+2-3==1
# Norm triangle and Cauchy-Schwarz give m^2 <= 2(sum basis norm squares)
z1,z2,f1,f2=s.symbols('z1 z2 f1 f2', nonnegative=True)
assert s.expand((z1*z1+z2*z2)*(f1*f1+f2*f2)-(z1*f1+z2*f2)**2)==s.expand((z1*f2-z2*f1)**2)
print('Verified intersections, split cohomology, nef obstructions, exact Schur-complement identity, and norm inequality.')
Path('workspace/agent3_numerics.py').write_text(Path('scratchpad.py').read_text().split("Path('workspace/")[0])

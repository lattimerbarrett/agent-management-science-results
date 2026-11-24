import sympy as s
r,p=s.symbols('r p', positive=True, real=True)
f=s.Function('f')
# Fiber t of line L, metric exp(-phi); squared norm rho=|t|² exp(-phi).
# At dphi=0 and t !=0, Levi rho = rho*(-Levi phi) on base and exp(-phi)>0 vertical.
# Curvature of M=L* is -Levi phi, so inertia: positive(rho Levi_M)+1.
a,b,e=s.symbols('a b e', integer=True)
def dot(D,F):
 a,b=D;c,d=F
 return s.expand(-e*a*c+a*d+b*c)
A=(5,-1);B=(-1,12*e+5);H=(1,3*e+1);P=(4,12*e+3)
assert dot(A,P)==40*e+11
assert dot(B,P)==40*e+17
assert dot(A,B)==65*e+26
assert dot((4,12*e+4),(4,12*e+4))==80*e+32
print('Checked A.P, B.P, c2, c1² symbolically for all e')
print('Scalar-model obstruction: if curvature(A)=5alpha-beta and curvature(B)=-alpha+5beta, horizontal eigenvalues at weight p are',6*p-1,5-6*p)
print('Both positive iff 1/6 < p < 5/6. A smooth fibre-profile derivative transitions 0 to1, hence cannot keep positive vertical curvature outside this interval.')
from pathlib import Path
# Local Finsler normal form at v=(r,0): explicitly verify inverse norm Hessian.
x1,y1,x2,y2,u1,w1,u2,w2,k1,k2=s.symbols('x1 y1 x2 y2 u1 w1 u2 w2 k1 k2', real=True)
vars=[(x1,y1),(x2,y2),(u1,w1),(u2,w2)]
G=s.exp(-k1*(x1*x1+y1*y1)-k2*(x2*x2+y2*y2))*(u1*u1+w1*w1+u2*u2+w2*w2)
psi=1/G
point={x1:0,y1:0,x2:0,y2:0,u1:r,w1:0,u2:0,w2:0}
def dz(expr,pair,bar=False):
 x,y=pair
 return (s.diff(expr,x)+(s.I if bar else -s.I)*s.diff(expr,y))/2
Levi=s.Matrix([[s.simplify(dz(dz(psi,a),b,True).subs(point)) for b in vars] for a in vars])
assert Levi==s.diag(k1/r**2,k2/r**2,1/r**4,-1/r**4)
print('Exact local Finsler inverse-norm Levi:',Levi)
# Dual-envelope local inertia identity, with arbitrary complex coefficients.
c=s.symbols('c', real=True)
dr,di=s.symbols('dr di', real=True);d=dr+s.I*di
br1,bi1,br2,bi2,er1,ei1,er2,ei2=s.symbols('br1 bi1 br2 bi2 er1 ei1 er2 ei2', real=True)
bv=s.Matrix([br1+s.I*bi1,br2+s.I*bi2]);ev=s.Matrix([er1+s.I*ei1,er2+s.I*ei2])
D=c*c-d*s.conjugate(d)
loss=(c*(bv*bv.H+ev*ev.H)-s.conjugate(d)*ev*bv.H-d*bv*ev.H)/D
Cv=(c*ev-d*bv)/D
gamma=c/D
assert (-loss+Cv*Cv.H/gamma+bv*bv.H/c).applyfunc(s.simplify)==s.zeros(2)
print('Full complex dual-envelope Schur identity verified: base Schur = A-b b*/c, independent of complex pure-Hessian d,e.')
Path('workspace/agent4_checks.py').write_text(Path('scratchpad.py').read_text())

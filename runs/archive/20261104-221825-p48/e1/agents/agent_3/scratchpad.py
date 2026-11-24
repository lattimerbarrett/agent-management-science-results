import sympy as s
from pathlib import Path
e=s.symbols('e',integer=True,nonnegative=True)
def dot(D,F):
 a,b=D;c,d=F
 return s.expand(-e*a*c+a*d+b*c)
A=(5,-1);B=(-1,12*e+5);H=(1,3*e+1);P=(4,12*e+3);C=(4,12*e+4)
assert dot(A,P)==40*e+11
assert dot(H,H)==5*e+2
assert dot(A,H)==dot(B,H)==2*dot(H,H)
# Uniform RC positivity at the split metric: both curvature matrices
# are complementary, with trace 4. Equal weights of alpha's eigenvectors
# make both line curvatures exactly 2, regardless of alpha's eigenvalues.
t=s.symbols('t',real=True)
xi=s.Matrix([1,1])/s.sqrt(2)
alpha=s.diag(t,4-t)
beta=4*s.eye(2)-alpha
assert (xi.T*alpha*xi)[0]==2
assert (xi.T*beta*xi)[0]==2
assert dot(B,P)==40*e+17
assert dot(C,C)==80*e+32
assert dot(A,B)==65*e+26
assert 4*dot(A,B)-dot(C,C)==180*e+72
a,b=s.symbols('a b',integer=True)
Q=(4-a,12*e+4-b)
length=s.expand(dot(A,B)-dot((a,b),Q))
assert s.expand(length.subs(a,2))==45*e+18
assert s.expand(length.subs(a,3))==32*e+14+2*b
# Explicit Calabi-coordinate correction for the split line HE metrics.
# eta=dt^theta-e*t*beta, omega=eta+c*beta, dd^c f=u' dt^theta-e*u beta.
t=s.symbols('t',real=True)
c=3*e+1
p=c-e*t
f=3*s.log(p)
u=t*(1-t)*s.diff(f,t)
alpha_vertical=5+s.diff(u,t)
alpha_base=-1-5*e*t-e*u
assert s.simplify(alpha_vertical+alpha_base/p)==4
# Off-diagonal deformation-space dimensions, checked by ruled-surface Leray.
U=sum((12+k)*e+5 for k in range(7))
Vdim=sum((13+k)*e+7 for k in range(5))
assert s.expand(U)==105*e+35
assert s.expand(Vdim)==75*e+35
assert s.expand(U+Vdim)==180*e+70
# H2 End split vanish by Serre duality: K-A+B has S coefficient -8;
# K-B+A = 4S-(13e+8)f, so all pushforward summands have negative degree.
for k in range(5):
 degree=-(13*e+8)-k*e
 assert degree.subs(e,0)<0
# Riemann-Roch check of relative evaluation bundles.
K=(-2,-e-2)
def add(D,F): return tuple(s.expand(x+y) for x,y in zip(D,F))
def chi_twist(t):
 ct=add(C,(2*t,0))
 c2t=dot(A,B)+t*dot(C,(1,0))+t*t*dot((1,0),(1,0))
 return s.expand(2+dot(ct,add(ct,tuple(-x for x in K)))/2-c2t)
assert chi_twist(-1)==-23*e-6
assert chi_twist(-1)-4==-23*e-10
assert chi_twist(-2)==-33*e-12
# Nonzero angular gradient does NOT suffice for regularized-min inertia.
D=s.diag(1,1,1,-1); w=s.Matrix([2,0,0,1]); Dmin=D-w*w.T
badblock=Dmin.extract([0,3],[0,3])
assert badblock.det()==2 and s.trace(badblock)==-5
assert Dmin[1,1]==Dmin[2,2]==1
# Vertical Hessian of inverse homogeneous Finsler G: exact sample with rational positive g.
g=s.Matrix([[2,1],[1,3]]);v=s.Matrix([1,2]);G=(v.T*g*v)[0]
p=g*v
V=-g/G**2+2*(p*p.T)/G**3
assert V.det()<0
assert (v.T*V*v)[0]==1/G
# Euler/projector identity: eigenvalues after g-normalized congruence are +/-1/G^2.
T=-s.eye(2)+2*v*p.T/G
assert T.charpoly().as_expr().expand()==s.Symbol('lambda')**2-1
print('All symbolic intersection, discriminant, canonical-extension length, H2 vanishing, and inverse-Finsler inertia checks passed.')
Path('workspace/agent3_numerics.py').write_text(Path('scratchpad.py').read_text())
import sympy as s
# Intersection ring checks, valid symbolically for every e>=0.
e=s.symbols('e', integer=True, nonnegative=True)
def pair(a,b):
    return s.expand(-e*a[0]*b[0]+a[0]*b[1]+a[1]*b[0])
H=(1,3*e+1); P=(4,12*e+3)
A=(5,-1); B=(-1,12*e+5)
c1=(4,12*e+4); D=(3,-6*e-3)
assert pair(H,H)==5*e+2
assert pair(A,B)==65*e+26
assert pair(c1,c1)==80*e+32
assert pair(c1,c1)-pair(A,B)==15*e+6
assert pair(D,D)==-45*e-18
assert pair(D,H)==0 and pair(D,P)==-3
assert pair(A,P)==40*e+11
assert pair(B,P)==40*e+17
assert pair(c1,P)/2==40*e+14
# A positive Hermitian curvature E produces negative curvature of L in
# both horizontal directions. Model normal-coordinate Levi inverse norm.
# For E metric exp(-|z|^2)I, coordinate r=|v|^2, psi=1/(exp(-|z|^2)r).
xs=s.symbols('x0:4',real=True)
ys=s.symbols('y0:4',real=True)
psi=s.exp(xs[0]**2+ys[0]**2+xs[1]**2+ys[1]**2)/(xs[2]**2+ys[2]**2+xs[3]**2+ys[3]**2)
point={**{x:0 for x in xs},**{y:0 for y in ys},xs[2]:1}
# Actual Wirtinger differentiation, not an asserted sign matrix.
model=s.Matrix(4,4,lambda i,j:s.simplify((s.diff(psi,xs[i],xs[j])+s.diff(psi,ys[i],ys[j])+s.I*s.diff(psi,xs[i],ys[j])-s.I*s.diff(psi,ys[i],xs[j])).subs(point)/4))
assert model==s.diag(1,1,1,-1)
assert [s.sign(model[i,i]) for i in range(4)]==[1,1,1,-1]
print('Computed complex Hessian at (z,v)=(0,(1,0)):',model)
print('All intersection identities and curvature-sign checks passed symbolically for every e>=0.')
print('H^2=',pair(H,H),' c1^2=',pair(c1,c1),' c2=',pair(A,B))
print('Griffiths-positive inverse-norm model Levi signs: +,+,+,- (kappa <= 2).')
# Numerical Chern ratio is compatible even with strict pointwise Griffiths positivity.
t=s.sqrt(3)/2
R11=s.diag((1+t)/2,(1-t)/2)
R22=s.diag((1-t)/2,(1+t)/2)
R12=s.Matrix([[0,0],[t,0]])
R21=R12.T
c2local=s.simplify(s.trace(R11)*s.trace(R22)-s.trace(R12)*s.trace(R21)-s.trace(R11*R22)+s.trace(R12*R21))
c1sq_local=2
assert s.simplify(c2local/c1sq_local)==s.Rational(13,16)
assert 0<t<1
# R(x,x)=(1-t)|x|²I/2+t*xbar*xbar^*, strictly positive for x!=0.
print('Strictly Griffiths-positive algebraic curvature tensor attains c2/c1²=13/16.')
from pathlib import Path
Path('workspace/agent1_checks.py').write_text(Path('scratchpad.py').read_text().split('from pathlib import Path')[0])
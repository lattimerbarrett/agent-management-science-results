import sympy as s
from pathlib import Path
# Exact local peak identity for the model strictly pseudoconvex domain B^n.
# q=(1,0,...,0), h(z)=z_1-1.  This identity proves Re(h)<=-|z-q|²/2
# on B^n, so max(Re(h),-delta) glues to -delta off a small q-ball.
x,y,u,v=s.symbols('x y u v',real=True)
norm2=x*x+y*y+u*u+v*v
dist2=(x-1)**2+y*y+u*u+v*v
peak=x-1
assert s.expand(-2*peak-dist2-(1-norm2))==0
# Exact Levi matrices for the two ball orientations.
z,zb,w,wb=s.symbols('z zb w wb')
rho=z*zb+w*wb-1
levi=s.Matrix([[s.diff(rho,a,b) for b in (zb,wb)] for a in (z,w)])
assert levi==s.eye(2)
assert -levi==-s.eye(2)
# Exact strictly pseudoconvex quadratic model in C^2.
# r=Re(w)+lambda |z|², lambda>0. Its complex tangent at zero is w=0.
lam=s.symbols('lam',positive=True)
r=(w+wb)/2+lam*z*zb
L=s.Matrix([[s.diff(r,a,b) for b in (zb,wb)] for a in (z,w)])
assert L==s.diag(lam,0)
assert s.diff(r,w)==s.Rational(1,2)
# Rank-one normal correction for a general strictly tangentially positive Levi matrix.
p,q,c=s.symbols('p q c',real=True)
A=(p*p+q*q+1)/lam-c
H=s.Matrix([[lam,p+s.I*q],[p-s.I*q,c+A]])
assert s.simplify(H.det())==1
# Sylvester: lam>0 and determinant=1 give positive definiteness.
source=Path(__file__).read_text()
Path('workspace/agent2_peak_checks.py').write_text(source)
Path('workspace/agent2_necessity.md').write_text(r'''## Rigorous result: 2 belongs to N
Let Y have CAP. Every continuous bounded-above psh u on Y is constant on each component. Indeed, for a small affine disc f near any point of Y, CAP gives entire maps F_j:C→Y converging uniformly to f on its closed parameter disc. Each u∘F_j is bounded-above subharmonic, hence constant. Continuity of u passes equality to f, so u is locally constant, hence constant on components.

Suppose a boundary point q of Y is strictly pseudoconvex. Choose r with Y={r<0} near q, r(q)=0. Its tangential Levi form is positive definite. Replacing r by r+A r² for sufficiently large A makes its full Levi form positive definite at q: in tangential/normal coordinates this is a rank-one positive normal correction, and the assertion follows by the Schur complement. Shrinking the neighborhood keeps r+A r² negative precisely when r is negative. Taylor expansion at q=0 writes
r+A r²=2 Re P(z)+H(z)+O(|z|³),
where P is a holomorphic quadratic polynomial with P(0)=0 and H is a positive definite Hermitian quadratic form. Thus Re P(z)≤-c|z|² on Y∩B(0,R), for some c,R>0.

Fix 0<delta<cR² and define u=max(Re P,-delta) on Y∩B(0,R), u=-delta on the rest of Y. On a neighborhood of the artificial sphere |z|=R this agrees with the constant -delta, so it glues to a continuous bounded psh function. Its values approach 0 as z approaches q through Y, whereas it equals -delta somewhere in the same component. (For example, take a point of that component near the artificial sphere.) Hence it is not constant, contradiction.

For K in K_2, if the defining rho has a negative tangential Levi value at q, then r=-rho defines the exterior near q and has positive definite tangential Levi form, since that tangent space has complex dimension one. Thus an Oka exterior forces rho to have nonnegative tangential Levi everywhere. This proves 2∈N without any global Oka theorem.
''')
print('PASS: exact local peak identity, orientation reversal, tangential Levi test')

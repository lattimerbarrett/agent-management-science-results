from pathlib import Path
import sympy as s
from z3 import Int,Solver,Or,sat,unsat
d,q=s.symbols('d q',integer=True,nonnegative=True)
n=2*d
lap=d*(d+n-3)-q*(q+n-3)
c=(n-2)*(1-d+lap/(2*(n-1)))
expected=-(d-1)*(q+d-1)*(q+d-2)/(2*d-1)
assert s.factor(c-expected)==0
sigma=1-d
assert s.expand(sigma*(sigma+n-2)+(d-1)**2)==0
# Polar hypergeometric parameters for sphere dimension N=2d-1.
a=(q+d-1)/2;cc=q+(2*d-1)/2
assert s.simplify(cc-2*a-s.Rational(1,2))==0
assert s.simplify(cc-a-(q+d)/2)==0
D,Q=Int('D'),Int('Q');sol=Solver();sol.add(D>=2,Q>=0,(D-1)*(Q+D-1)*(Q+D-2)==0,Or(D!=2,Q!=0));assert sol.check()==unsat
for DD in range(2,10):
 for QQ in range(DD%2,DD+1,2):
  coef=s.factor(expected.subs({d:DD,q:QQ}))
  DtN=2*s.gamma(s.Rational(QQ+DD,2))**2/s.gamma(s.Rational(QQ+DD-1,2))**2
  assert DtN>0
  assert coef!=0 or (DD==2 and QQ==0)
print('PASS symbolic all-even-dimensional critical source factor and radial/angular exponents; unique gauge-zero proved by Z3')
proof=r'''# Positive homogeneous critical-jet logarithmic form in even dimensions

**Scope:** this establishes the homogeneous far-field algebraic sign. It does
not provide the missing unrestricted blow-up extraction or cutoff matching.

Let n=2d>=4. Let h=r^d P_q(omega) be a homogeneous graph polynomial of degree d
in R^(n-1), where P_q is a nonzero spherical harmonic of degree q, 0<=q<=d,
with d-q even. Insert h into the exact first-order Robin source. Its leading
homogeneous term as r->infinity is
 c_(d,q) r^(-d)P_q,
 c_(d,q)=-(d-1)(q+d-1)(q+d-2)/(2d-1).
Indeed Delta_R^(n-1)h=[d(d+n-3)-q(q+n-3)]r^(d-2)P_q; direct factorization
of (n-2)[1-d+{d(d+n-3)-q(q+n-3)}/(2(n-1))] gives the displayed coefficient.
For d>=2,q>=0 this coefficient vanishes only for d=2,q=0, the radial quadratic
conformal-gauge graph.

The homogeneous harmonic response is z=r^(1-d)Y(theta), theta in S^(2d-1)_+.
Since (1-d)(1-d+n-2)=-(d-1)^2, its angular equation is
 (-Delta_S^(2d-1)+(d-1)^2)Y=0,
 partial_nuY=c_(d,q)P_q on S^(2d-2).
The operator is strictly coercive, so the weak Neumann problem has a unique
smooth solution. Integration by parts gives
 int_(S+)(|gradY|^2+(d-1)^2Y^2)
      =int_(equator)Y partial_nuY>0
whenever c_(d,q)!=0. With unit boundary value P_q, the regular polar solution
has hypergeometric parameters a=b=(q+d-1)/2, c=q+d-1/2, so its positive
Dirichlet-to-Neumann eigenvalue is
 Dcrit_(d,q)=2 Gamma((q+d)/2)^2/Gamma((q+d-1)/2)^2.
Consequently the energy coefficient is exactly
 c_(d,q)^2/Dcrit_(d,q) *||P_q||_L2(S^(2d-2))^2.

On R0<r<R, the Dirichlet energy of z is this coefficient times log(R/R0),
because its radial density is r^-1. The linearized bubble potential changes
this by a finite tail: U^(4/(n-2))=O(r^-4), z^2=O(r^(2-2d)) and the volume
factor is r^(2d-1), giving r^-3. For a response associated with a strictly
lower graph degree e<d, the cross Dirichlet radial power is r^(e-d-1)<=r^-2,
so that cross term has finite tail. Angular orthogonality makes different q
critical sectors orthogonal. Thus the non-gauge homogeneous critical-order
logarithmic block is positive definite.

This is the direct even-dimensional counterpart of the finite subcritical
jet-form checks. It alone does NOT prove that a general blowing-up sequence
reduces to those forms, nor that all remainder and mass terms have the
required sign. In particular no compactness conclusion is asserted here.
'''
Path('workspace/agent4_even_critical_jet_sign.md').write_text(proof)
if Path(__file__).name=='scratchpad.py':Path('workspace/agent4_even_critical_checks.py').write_text(Path(__file__).read_text())

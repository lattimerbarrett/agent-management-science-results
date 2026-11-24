import sympy as s
from z3 import Real, Solver, unsat
eta,t=Real('eta'),Real('t')
S=Solver(); S.add(eta>s.Rational(1,2),t>=eta,t<=1-eta)
assert S.check()==unsat
S=Solver(); S.add(eta==s.Rational(1,2),t>=eta,t<=1-eta,t!=s.Rational(1,2))
assert S.check()==unsat
N=s.symbols('N', integer=True, positive=True)
e=s.symbols('eta', positive=True)
a0,aN=s.symbols('a_0 a_N')
# Formal exact telescoping coefficient vector for trace-additive case.
for n in range(1,101):
    a=s.symbols('a:'+str(n+1))
    assert s.expand(sum(a[j+1]-a[j] for j in range(n))-(a[-1]-a[0]))==0
print('Verified eta>1/2 contradiction; eta=1/2 forces scalar plateau; exact telescoping n=1..100.')
# Exact rational graph-projection inequalities used in the completeness argument.
for Y in [s.Matrix([[0,0],[0,0]]), s.eye(2),s.Matrix([[s.Rational(1,2),s.Rational(1,3)],[0,s.Rational(1,2)]]), s.Matrix([[0,1],[0,0]])]:
    I=s.eye(2)
    assert (I-Y.T*Y).is_positive_semidefinite
    V=I.col_join(Y)
    P=V*(V.T*V).inv()*V.T
    assert P*P==P and P.T==P
    D=s.diag(2,2,s.Rational(2,3),s.Rational(2,3))
    assert (D-P).is_positive_semidefinite
    aa,bb,cc,dd=P[:2,:2],P[:2,2:],P[2:,:2],P[2:,2:]
    assert (aa-s.eye(2)/2).is_positive_semidefinite
    assert cc*aa.inv()==Y
    assert dd-cc*aa.inv()*bb==s.zeros(2)
print('Verified rational graph-projection identities and order bounds in 4 exact cases.')
# Stably finite norm-ultraproducts need not have hyponormal rigidity.
for n in range(2,41):
    w=[s.Integer(0)]+[s.Rational(n-j,n-1) for j in range(1,n)]
    comm=[w[j]-w[(j-1)%n] for j in range(n)]
    assert comm.count(s.Integer(1))==1
    assert comm.count(-s.Rational(1,n-1))==n-1
    assert sum(comm)==0 and max(w)==1
print('Verified weighted cyclic-shift positive/negative selfcommutator spectrum n=2..40.')
# Free-algebra verification: Schur residual r=d-c*a^{-1}*b is a projection
# whenever [[a,b],[c,d]] is a projection and a is invertible.
from collections import defaultdict
rules={('d','d'):{('d',):1,('c','b'):-1},
       ('d','c'):{('c',):1,('c','a'):-1},
       ('b','d'):{('b',):1,('a','b'):-1},
       ('b','c'):{('a',):1,('a','a'):-1},
       ('a','A'):{():1},('A','a'):{():1}}
def reduce_word(w):
    for i in range(len(w)-1):
        pair=w[i:i+2]
        if pair in rules:
            out=defaultdict(int)
            for v,k in rules[pair].items():
                for z,h in reduce_word(w[:i]+v+w[i+2:]).items(): out[z]+=k*h
            return {z:h for z,h in out.items() if h}
    return {w:1}
def reduce_poly(poly):
    out=defaultdict(int)
    for w,k in poly.items():
        for z,h in reduce_word(w).items():out[z]+=k*h
    return {w:k for w,k in out.items() if k}
r={('d',):1,('c','A','b'):-1}
r2=defaultdict(int)
for u,k in r.items():
    for v,h in r.items():r2[u+v]+=k*h
for u,k in r.items():r2[u]-=k
assert reduce_poly(r2)=={}
print('Verified Schur residual projection identity in the free algebra.')
# Modulus domination |q(x)|<=q(|x|), even for accretive-sectorial x,
# would imply full additivity; verify the asymptotic algebra exactly.
t0=s.symbols('t0',positive=True)
hh,kk=s.symbols('hh kk',commutative=False)
XX=t0+hh+s.I*(t0+kk)
XXstar=t0+hh-s.I*(t0+kk)
assert s.expand(XXstar*XX-(2*t0**2+2*t0*(hh+kk)+hh**2+kk**2+s.I*(hh*kk-kk*hh)))==0
approx=s.sqrt(2)*t0+(hh+kk)/s.sqrt(2)
assert s.expand(approx**2-(2*t0**2+2*t0*(hh+kk)+(hh+kk)**2/2))==0
u,v=s.symbols('u v',real=True)
assert s.simplify(s.limit(s.sqrt((t0+u)**2+(t0+v)**2)-s.sqrt(2)*t0,t0,s.oo)-(u+v)/s.sqrt(2))==0
print('Verified exact asymptotic algebra obstructing modulus domination.')

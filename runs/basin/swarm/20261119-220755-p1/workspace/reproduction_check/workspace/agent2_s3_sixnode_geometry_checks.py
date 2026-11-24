"""Exact finite checks of the six-positive-node cubic-stratum geometry."""
import itertools
import sympy as S
import z3
lam=list(map(S.Rational,[0,1,2,3,4,5]))
d=[S.prod(a-b for b in lam if b!=a) for a in lam]
# Monic cubic with exactly one zero in each alternating node gap.
f_sign=[-1,1,1,-1,-1,1]
d_sign=[S.sign(v) for v in d]
assert [a*b for a,b in zip(f_sign,d_sign)]==[1,1,-1,-1,1,1]
sets=[]
for mu in [S.Rational(1,2),S.Rational(5,2),S.Rational(9,2)]:
 # For P6(mu)=-2N<0, sign Lagrange ell_j equals sign(-1/((mu-lambda_j)d_j)).
 negative_facets={j+1 for j in [1,2,3,4] if (mu-lam[j])*d[j]>0}
 sets.append(negative_facets)
assert sets==[{3,5},{2,5},{2,4}]
print('PASS exact H-sign and negative-probe facet-star tables:', sets)
a,b=z3.Reals('a b')
box=z3.And(a>=0,a<=1,b>=0,b<=1)
star={1:z3.Or(a==1,b==1),3:z3.Or(a==0,b==1),5:z3.Or(a==0,b==0)}
def proves(stmt):
 s=z3.Solver();s.add(box,z3.Not(stmt));assert s.check()==z3.unsat
proves((z3.And(star[1],star[5]))==z3.Or(z3.And(a==1,b==0),z3.And(a==0,b==1)))
proves(z3.And(star[1],star[3])==(b==1))
proves(z3.And(star[3],star[5])==(a==0))
B=z3.Real('B');A=z3.Real('A')
# Fixed extreme coordinate plus its star gives a point or a single edge.
proves(z3.Implies(z3.And(star[1],b==B,B<1),a==1))
proves(z3.Implies(z3.And(star[5],a==A,A>0),b==0))
proves(z3.Implies(z3.And(star[3],b==B,B<1),a==0))
proves(z3.Implies(z3.And(star[3],a==A,A>0),b==1))
print('PASS exact Z3 facet-star intersections and fixed-extreme-coordinate reductions')
# Generic monic-degree-six interpolation identity, with a rational test node.
x,mu=S.symbols('x mu');cs=S.symbols('c0:6')
K=x**6+sum(cs[j]*x**j for j in range(6));P=S.prod(x-a for a in lam)
ell=[S.prod((mu-b)/(a-b) for b in lam if b!=a) for a in lam]
assert S.cancel(K.subs(x,mu)-P.subs(x,mu)-sum(l*K.subs(x,a) for l,a in zip(ell,lam)))==0
print('PASS generic monic-sextic Lagrange interpolation identity')

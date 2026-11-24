"""Exact constants for the greedy-clique mixed book lemma."""
import sympy as S
rt=S.sqrt(3)
u0=1/(2*rt)
u1=4/rt-2
astar=S.expand(u1*u1)
C0=S.Rational(7,4)-rt/2
c0=2*rt-3
assert S.Rational(1,12)<astar<S.Rational(12,125)
assert S.simplify(3-c0/u1)==S.Rational(3,2)
assert S.simplify(2/(rt*u1)-2)==rt
u=S.symbols('u',positive=True)
lam=2/(rt*u)-2
kap=3-c0/u
t=2*rt*u
K=3-t
assert S.simplify(1-lam/2+kap/3-(3-(rt-1)/u))==0
assert S.simplify(3-K-kap*u*u-((4*rt-3)*u-3*u*u))==0
assert S.diff(kap,u)>0
assert S.diff(3-(rt-1)/u,u)>0
const=(4*rt-3)*u-3*u*u
assert S.simplify(S.diff(const,u).subs(u,u1))>0
assert S.simplify(const.subs(u,u0)-C0)==0
assert S.simplify((3-(rt-1)/u).subs(u,u0)-c0)==0
z1,z2,z3=S.symbols('z1 z2 z3',nonnegative=True)
quart=(z1*z1+z2*z2+z3*z3)**2-3*z1*z2*z3*(z1+z2+z3)
sos=S.Rational(1,2)*((z1*z1-z2*z2)**2+(z2*z2-z3*z3)**2+(z3*z3-z1*z1)**2)+S.Rational(3,2)*((z1*z2-z2*z3)**2+(z2*z3-z3*z1)**2+(z3*z1-z1*z2)**2)
assert S.expand(quart-sos)==0
Q,Z=S.symbols('Q Z',nonnegative=True)
Ssum=S.symbols('Ssum',nonnegative=True)
f0=3-K-kap*u*u-2*Ssum+(1-lam/2+kap/3)*Q+lam*Ssum*Ssum/2
completed=(Ssum-3*u)**2/(3*u)+(3-(rt-1)/u)*(Q-Ssum*Ssum/3)+3*u*(u1-u)
assert S.simplify(f0-completed)==0
# For high Q use the same coarse constants in both parameter regimes.
# If Q>=sqrt(1/C), minimize C0-2z+c0 Q+sqrt(3)/2 z^2 over z>=Q.
for C,d in [(S.Rational(11,6),S.Rational(18,125)),(S.Rational(5,3),S.Rational(1,6))]:
 q0=S.sqrt(1/C); q1=2/rt
 linear=C0-2/rt+c0*Q-d*(C*Q*Q-1)
 assert S.simplify(linear.subs(Q,q0))>0
 assert S.simplify(linear.subs(Q,q1))>0
 quadratic=C0+(c0-2)*Q+rt*Q*Q/2-d*(C*Q*Q-1)
 poly=S.Poly(quadratic,Q)
 assert poly.nth(2)>0
 assert S.discriminant(poly.as_expr(),Q)<0
# Frozen-parameter random-branch comparison on [u1,1/3].
Kstar=4*rt-5
random_gap=Kstar/3-rt*u*u-u*u*(u*u-astar)/2-(1-u)**2
assert S.simplify(random_gap.subs(u,u1))==0
assert S.simplify(random_gap.subs(u,S.Rational(1,3)))>0
assert S.diff(random_gap,u,2).subs(u,0)<0
assert S.expand(S.diff(random_gap,u,2)).coeff(u,2)<0
# Frozen correction constant <=5/3.
tstar=4/(2+rt)
assert S.simplify(S.Rational(3,2)/(3*tstar)+1/(9*astar))<S.Rational(5,3)
# lambda_i stays in [0,2] in both regimes.
assert S.Rational(9,8)+S.Rational(1,6)<2
# k2-terminal factor used in the proof.
x=S.symbols('x')
g=S.Rational(1,2)+x*x*(S.Rational(1,2)+x*x-2*x)-(1-x)**2
assert S.factor(g)==(x-1)*(x+1)*(2*x*x-4*x+1)/2
if __name__=='__main__':
 print('ALL EXACT GREEDY MIXED-LEMMA CERTIFICATES PASSED')
 print('a* =',astar)

"""Exact comparison needed to extend the mixed-root bound beyond crossover."""
import sympy as s
u=s.symbols('u',real=True)
t=s.sqrt(3);q=4*t/3-2;A=s.expand(q*q);K=4*t-5
L=K/3-t*u*u-u*u/2*(u*u-A)
g=(1-u)**2
P=u**3+q*u*u+(2+2*t)*u-4*t/3
assert s.simplify(L-g+(u-q)*P/2)==0
assert s.simplify(P.subs(u,s.Rational(1,3))-(13-14*t)/27)==0
assert q>0 and q<s.Rational(1,3)
assert (13-14*t)/27<0
# P'(u)=3u²+2q*u+2+2sqrt3>0 for u>=0.
assert s.simplify(s.diff(P,u)-(3*u*u+2*q*u+2+2*t))==0
# Thus for q<u<=1/3, P(u)<0 and L-g>0; equality at q.
print('High-middle exact factorization passed:')
print('L-g = -(u-q*) P(u)/2')
print('P(1/3) =',s.simplify(P.subs(u,s.Rational(1,3))))

import sympy as S
z=S.symbols('z');P=3*z**4+3*z**3-10*z*z+6*z-1
assert P.subs(z,S.Rational(1,3))==S.Rational(1,27)
assert P.subs(z,S.Rational(1,2))==S.Rational(1,16)
assert S.diff(P,z,2).subs(z,S.Rational(1,2))==-2
# P'' is increasing on the interval, so endpoint gives a uniform negative bound.
assert S.expand(S.diff(P,z,3)-(72*z+18))==0
c=2*z-z*z;a=z*z;ratio=z*z/(1-z)**2
E=2*c-1+a*(1-3*z/(1-z)+ratio)
assert S.factor(E*(1-z)**2-P)==0
k,a,c,t,L=S.symbols('k a c t L')
assert S.expand((t*L+k)**2-a*L*L-2*L-((t*t-a)*L*L+(2*k*t-2)*L+k*k))==0
print('High-range greedy-triangle polynomial and weighted-clique contradiction checked exactly.')

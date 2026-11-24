import sympy as s
A,B=s.symbols("A B",positive=True)
# FS density for gamma(z)=(exp(z),exp(i*z)).
num=s.expand((1+A+B)*(A+B)-(A*A+B*B))
assert s.expand(num-(A+B+2*A*B))==0
# Exact lower bound on disjoint source discs about 2*pi*i*k, k>=1:
# A in [1/2,2], B in [0,1/2], density >= (1/2)/(7/2)^2=2/49.
assert s.Rational(1,2)/s.Rational(7,2)**2==s.Rational(2,49)
assert s.exp(s.Rational(1,4)).evalf()<2
assert s.exp(-s.Rational(1,4)).evalf()>s.Rational(1,2)
assert s.exp(-4*s.pi+s.Rational(1,4)).evalf()<s.Rational(1,2)
print("FS density exact identity verified:",num/(1+A+B)**2)
print("Uniform local density lower bound on infinitely many disjoint discs: 2/49")

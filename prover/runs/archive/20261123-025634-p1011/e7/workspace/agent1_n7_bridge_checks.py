import sympy as s
n=s.Integer(7);a=(n-2)/2;p=(n+2)/(n-2);k=s.Integer(2)
assert a==s.Rational(5,2) and p==s.Rational(9,5)
assert a*p-n==-a
assert a+k==s.Rational(9,2)
assert 1-a-k==-s.Rational(7,2)
assert 1/(k*(p-1))==s.Rational(5,8)
r=s.symbols("r",positive=True); A,B=s.symbols("A B")
assert s.diff(r**a*(A*r**(2-n)+B),r).subs(r,1)==a*(B-A)
assert 3>(n-2)/2
assert (n-2)-8==-3
print("n7 conditional bridge exponents, second-critical-radius identity, and AF integrability checks passed")

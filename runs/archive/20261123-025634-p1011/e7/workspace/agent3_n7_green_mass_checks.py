import sympy as s
f,D=s.symbols('f D')
for k,target in [(4,s.Rational(5,3)*f-s.Rational(5,12)*D),(5,s.Rational(5,4)*f-s.Rational(5,12)*D),(6,-s.Rational(5,12)*D)]:
 source=5*(k-1)*f-s.Rational(5,12)*(D+k*(k+4)*f)
 assert s.simplify(source-target)==0
assert s.Rational(5,3)/6==s.Rational(5,18)
assert -s.Rational(15,2)*s.Rational(5,18)==-s.Rational(25,12)
assert s.Rational(25,4)*s.Rational(2,3)==s.Rational(25,6)
print('n7 GM diagnostic source, mean, Pohozaev and mass coefficients checked')

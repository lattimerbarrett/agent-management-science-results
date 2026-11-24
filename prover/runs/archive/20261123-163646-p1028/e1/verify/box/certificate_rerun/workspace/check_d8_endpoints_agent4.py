import sympy as s
G=s.Rational(139,360)
for a in range(9,14):
 E=s.Rational(2,16-a)
 assert s.Rational(a,8)-s.Rational(1,4)-E>=G
for a in range(9,13):
 E=s.Rational(13,8*(14-a))
 assert s.Rational(a,8)-s.Rational(1,4)-E>=G
assert s.Rational(13,8)-s.Rational(1,4)-s.Rational(71,72)>=G
assert s.Rational(13,8)-s.Rational(1,4)-s.Rational(11,12)>=G
assert s.Rational(14,24)-s.Rational(7,36)>=G
assert 36+s.Rational(60**2+72**2,48)+72==291>288
A=s.symbols('A',positive=True)
W=6*A-3
assert s.simplify(W**2/(2*A)+W-24*(A-1))==3+s.Rational(9,2)/A
print('all d8 endpoint rational and DAG inequalities checked')

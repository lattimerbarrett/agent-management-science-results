import sympy as S
n,d=S.symbols('n d',positive=True)
A=d*(d+7)/(d+1)**2
assert S.simplify(S.diff(A,d)-(7-5*d)/(d+1)**3)==0
assert A.subs(d,9)==S.Rational(36,25)
assert A.subs(d,8)==S.Rational(40,27)
assert S.simplify(S.Rational(3,2)*n-S.Rational(33,4)-(A.subs(d,8)*n-8))==n/S.Integer(54)-S.Rational(1,4)
assert S.Rational(14,54)-S.Rational(1,4)>0
print('Exact d>=8 coefficient and threshold checks passed')

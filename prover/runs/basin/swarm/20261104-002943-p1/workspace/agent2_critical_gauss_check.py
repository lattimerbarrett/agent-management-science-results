import sympy as S
mu=[-S.sqrt(5+2*S.sqrt(2)),-S.sqrt(5-2*S.sqrt(2)),S.sqrt(5-2*S.sqrt(2)),S.sqrt(5+2*S.sqrt(2))]
x=[-3,-S.sqrt(5),-1,1,S.sqrt(5),3]
w=[S.Rational(1,8),S.Rational(1,4),S.Rational(1,8),S.Rational(1,8),S.Rational(1,4),S.Rational(1,8)]
for j in range(8):
    assert S.simplify(sum(a**j for a in mu)/4-sum(wi*a**j for wi,a in zip(w,x)))==0
print('Exact equal Gauss/reference moments through degree7 verified.')

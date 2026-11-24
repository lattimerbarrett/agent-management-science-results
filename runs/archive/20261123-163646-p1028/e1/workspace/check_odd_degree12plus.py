import sympy as S
d,n=S.symbols('d n',positive=True)
A=(d+13)/(2*(d+1)**2);Q=(d+3)/(2*(d+1)**2);C=S.Rational(1,2)+6/(d+1)**2
assert S.factor(A*(d+1)-Q*(d-2))==(13*d+19)/(2*(d+1)**2)
assert S.factor(A+d*Q-C)==d/(d+1)**2
expr=S.factor(d*(A*n+(A+d*Q-C)*(n-1)/d-(A+d*Q)))
coef=d*(d+15)/(2*(d+1)**2);const=d*(d*d+4*d+15)/(2*(d+1)**2)
assert S.simplify(expr-(coef*n-const))==0
assert S.simplify(1-coef-(d*d-11*d+2)/(2*(d+1)**2))==0
print('constantderivative',S.factor(S.diff(const,d)))
assert const.subs(d,12)>S.Rational(278,45)
print('All exact d>=12 reduction algebra checks passed')

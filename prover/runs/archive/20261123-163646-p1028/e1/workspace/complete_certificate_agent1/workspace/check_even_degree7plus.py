import sympy as S
d,n=S.symbols('d n',positive=True)
r0=2/(d+1); g=2/(d*(d+1)*(d+2)); ell=3*n/(d+1)-1
bound=S.factor(d*(n-1-(d*n/2-ell)*r0-(3*n/2-ell)*g))
B=(d*d+8*d+3)/((d+1)*(d+2))
assert S.simplify(bound-(B*n-d-2+2/(d+2)))==0
assert S.simplify(S.Rational(3,2)-B-d*(d-7)/(2*(d+1)*(d+2)))==0
assert S.Rational(79,9)>S.Rational(33,4)
assert S.simplify(2*(d-3)/(d-1)-1-(d-5)/(d-1))==0
print('All exact Foster/twin coefficient checks passed')

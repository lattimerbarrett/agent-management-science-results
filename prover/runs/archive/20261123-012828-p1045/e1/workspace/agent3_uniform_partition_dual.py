"""Exact checks for the uniform greedy partition scalar dual.
The theta-symmetrization required to apply this remains unproved.
"""
import sympy as S
p,r=S.symbols('p r',positive=True);h=S.sqrt(3);a=p*p/3;s=1-r
nu=(p+h-2)/p
A=1-(1-p)*r;B=h-2*(1-p)*r
F=2*p*(1-p)*s/3+2*p*s/(3*A)+p*r/B+nu*r*(a-r)/s
g3=2*p*(2-p)/3;gh=2*p/h-p*p/3
assert S.simplify(F.subs(r,0)-g3)==0
assert S.simplify(S.diff(F,r).subs(r,0)-(gh-g3))==0
expected=-4*p*p*(1-p)/(3*A**3)+4*p*h*(1-p)/B**3-2*nu*(1-a)/(1-r)**3
assert S.simplify(S.diff(F,r,2)-expected)==0
# Valid for p in[1/2,1/sqrt3], a in[1/12,1/9], r in[0,a]:
# p<=3/5, h<=7/4, 1-p<=1/2, B>=h-r>=17/10-1/9>3/2.
# nu>=2*h-3>=2/5 and1-a>=8/9.
pos_bound=4*S.Rational(3,5)*S.Rational(7,4)*S.Rational(1,2)/S.Rational(3,2)**3
neg_bound=2*S.Rational(2,5)*S.Rational(8,9)
assert pos_bound==S.Rational(28,45)
assert neg_bound==S.Rational(32,45)
assert S.Rational(17,10)-S.Rational(1,9)>S.Rational(3,2)
assert S.Rational(3,5)**2>S.Rational(1,3)
assert S.Rational(7,4)**2>3>S.Rational(17,10)**2
print('uniform-partition dual: exact endpoint, derivative, concavity and rational bound checks passed')

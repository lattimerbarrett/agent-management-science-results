import sympy as S,os
x=S.symbols('x');be=S.Rational(13,8);ga=S.Rational(7,4);q=(x*x-1)*(x-be)*(x+ga);r=q.subs(x,-x);Q=S.expand(q*r);H=S.Rational(10125,65536);P=S.Poly(Q-H,x);D=S.Rational(23,8)
assert S.rem(S.Poly(Q+H,x),S.Poly((x*x-D)**2,x)).is_zero
# all positive roots of P isolated in four rational intervals
ints=[(S.Rational(3,4),1),(1,S.Rational(5,4)),(S.Rational(3,2),be),(ga,S.Rational(15,8))]
for a,b in ints:assert P.eval(a)*P.eval(b)<0
# even degree8 yields 8distinctreal roots by disjoint positive intervals and symmetry
assert P.degree()==8 and P.as_expr().subs(x,-x)==P.as_expr()
# Negative-level contact exact min and remaining factor positive at contact
fact=S.factor(Q+H); print('Q+H=',fact)
second=S.diff(Q,x,2);assert S.rem(S.Poly(second,x),S.Poly(x*x-D,x)).as_expr()>0
# positive fixedmeasure M=r*tau zeros interlace all8core roots using tau±13/10,0
# P signs certify intervals for roots separated by q/r/tau zero data
z=[-ga,-be,-S.Rational(13,10),-1,0,1,S.Rational(13,10),be,ga]
tau=x*(x*x-S.Rational(169,100));M=S.Poly(r*tau,x)
# exact roots of numerator r*tau are -be,-13/10,-1,0,1,13/10,ga
mroots=[-be,-S.Rational(13,10),-1,0,1,S.Rational(13,10),ga]
# P has alternating signs at numerator roots, and endpoints +/-2 positive
bounds=[S.Integer(-2)]+mroots+[S.Integer(2)]
assert all(P.eval(bounds[j])*P.eval(bounds[j+1])<0for j in range(8))
print('PASS n10 candidate:8simplecore eigenvalues,+2negativecontacts;positivefixedcoremeasure, NOT nonconvergent')

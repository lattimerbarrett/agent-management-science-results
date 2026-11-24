import sympy as S
from pathlib import Path
x,t=S.symbols('x t')
q=(x*x-1)*(x-2)*(x+3)
r=(x*x-1)*(x+2)*(x-3)
P=S.expand(q*r-1)
tau=x*(x*x-S.Rational(9,4)); M=S.expand(r*tau)
intervals=[(-4,-3),(-2,-S.Rational(3,2)),(-S.Rational(3,2),-1),(-1,0),(0,1),(1,S.Rational(3,2)),(S.Rational(3,2),2),(3,4)]
for a,b in intervals:
    assert P.subs(x,a)*P.subs(x,b)<0
assert S.degree(P)==8
# Therefore exactly one simple real root in each interval.
zerosM=[-2,-S.Rational(3,2),-1,0,1,S.Rational(3,2),3]
for z in zerosM: assert M.subs(x,z)==0
for j,z in enumerate(zerosM):
    assert intervals[j][1] <= z <= intervals[j+1][0]
# Monic M degree7, interlacing implies w=M(lambda)/P'(lambda)>0 and sum=1.
# Derive moments directly by Laurent expansion M/P.
ser=S.series((M/P).subs(x,1/t),t,0,11).removeO().expand()
mom=[S.factor(ser.coeff(t,j+1)) for j in range(10)]
def E(f):
    return S.factor(sum(c*mom[j[0]] for j,c in S.Poly(S.expand(f),x).terms()))
assert mom[0]==1
for j in range(4):assert E(q*x**j)==0
assert E(q*q)==1
Mnext=S.expand(q*tau)
assert S.expand(S.rem(q*M,P,x)-tau)==0
assert S.expand(Mnext-q*S.rem(q*M,P,x))==0
print('Positive 8-node gcd2 s4 fixed pair, rational moments, and exact restart: PASS')
print('P=',P)
print('moments 0..8=',mom[:9])

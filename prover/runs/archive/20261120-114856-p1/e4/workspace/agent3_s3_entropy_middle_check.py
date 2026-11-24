from sage.all import *
R=PolynomialRing(QQ,'z');z=R.gen();p=z**3-7*z;Q=p*p-25;H=QQ(11);P=Q-H
nodes=list(map(QQ,[-3,-2,-1,1,2,3]));assert P==prod(z-a for a in nodes)
neg=sorted((Q+H).roots(AA,multiplicities=False));beta=neg[0];gamma=neg[-1]
assert -3<beta<-2 and 2<gamma<3
for index in [2,3]:
    xi=nodes[index]
    aa=(beta-xi)/(beta-gamma);bb=(gamma-xi)/(gamma-beta)
    assert aa>0 and bb>0 and aa+bb==1
    coeff=[]
    for li in nodes:
        Lb=AA(P(beta))/((beta-li)*P.derivative()(li))
        Lg=AA(P(gamma))/((gamma-li)*P.derivative()(li))
        coeff.append(aa*Lb+bb*Lg)
    assert coeff[index]==0
    other=3 if index==2 else 2
    assert coeff[other]<0
    assert all(coeff[j]>=0 for j in range(6) if j!=other)
print('PASS: exact algebraic two-outer-band entropy certificates isolate BOTH middle endpoints')

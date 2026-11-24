import sympy as s
T,z=s.symbols("T z")
c=s.Rational(1,10);x=[s.Rational(3,5),s.Integer(4)]
y=[(-131+s.sqrt(23561))/80,z]
ps=[T**i*(1-x[i]*T)*(1-y[i]*T)for i in range(2)]+[(1-c*T)*(T+x[0])*(T+x[1]),(T+c)*(T+y[0])*(T+y[1])]
D=s.Matrix([[s.Poly(p,T).nth(j)for j in range(4)]for p in ps]).det(method="domain-ge")
E=s.expand(D-(1+c*c)*s.prod((1+xx*xx)*(1+yy*yy)for xx,yy in zip(x,y)))
tr=s.simplify((E.subs(z,1)+E.subs(z,-1))/2)
assert s.simplify(tr-(15448037*s.sqrt(23561)-2360918447)/8000000)==0
assert 15448037**2*23561-2360918447**2==48704647395635200
J=lambda t:t-1/t
y1=(27+s.sqrt(26329))/160
for xx,yy in zip(x,[y[0],y1]):
    assert s.simplify(J(yy)-s.Rational(3,4)*J(xx)-s.Rational(1,4)*J(c))==0
print(tr, s.N(tr))

import sympy as s
e=s.symbols("e",integer=True,nonnegative=True)
def I(x,y):
 a,b=x;c,d=y
 return s.expand(-e*a*c+a*d+b*c)
H=(1,3*e+1);P=(4,12*e+3);A=(5,-1);B=(-1,12*e+5);D=(3,-6*e-3)
assert I(A,B)==65*e+26
assert I(H,H)==5*e+2
assert I(D,D)==-45*e-18
assert I(D,H)==0 and I(D,P)==-3
assert I(A,P)==40*e+11 and I(B,P)==40*e+17
# Exact elementary-transform Chern arithmetic, correcting rejected witness.
a,d,h=s.symbols("a d h")
C=2*a-4
c2=s.expand(a*a*h-2*a*C*h+d*h)
assert s.expand(c2-(d-3*a*a+8*a)*h)==0
required_d=3*a*a-8*a+13
assert s.expand(c2.subs(d,required_d))==13*h
qdegree=s.expand(2*a*C-required_d)
subdegree=s.expand(required_d-C*C)
assert qdegree==a*a-13
assert subdegree==-a*a+8*a-3
print("All agent2 exact checks passed")

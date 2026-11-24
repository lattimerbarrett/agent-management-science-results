import sympy as s
e=s.symbols('e', integer=True, nonnegative=True)
def dot(D,F):
 a,b=D; c,d=F
 return s.expand(-e*a*c+a*d+b*c)
H=(1,3*e+1); P=(4,12*e+3)
L1=(5,-1); L2=(-1,12*e+5)
print('H^2 =',dot(H,H))
print('c1(E).P =',dot((4,12*e+4),P))
print('L1.P =',dot(L1,P),'L2.P =',dot(L2,P))
print('Ext1(L2,L1) dimension =',sum(12*e+5+k*e for k in range(7)))
A=(1,-2*e-1); K=(-2,-e-2)
D=(-6,12*e+6)
chi=s.expand(1+(dot(D,D)-dot(D,K))/2)
print('Ext1(L1,L2) dimension =',-chi)
print('c2 =',dot(L1,L2))

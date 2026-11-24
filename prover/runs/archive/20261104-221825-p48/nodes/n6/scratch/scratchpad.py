import sympy as s
e=s.symbols('e', nonnegative=True, integer=True)
def dot(D,F):
 a,b=D;c,d=F
 return s.expand(-e*a*c+a*d+b*c)
H=(1,3*e+1)
P=(4,12*e+3)
c1=(4,12*e+4)
L1=(5,-1);L2=(-1,12*e+5)
for name,val in [('H^2',dot(H,H)),('P^2',dot(P,P)),('c1.P',dot(c1,P)),('L1.P',dot(L1,P)),('L2.P',dot(L2,P)),('c1^2',dot(c1,c1)),('c2',dot(L1,L2))]:
 print(name, '=', val)
print('L1^2 =',dot(L1,L1))
print('L2^2 =',dot(L2,L2))
print('(L1-L2)^2 =',dot((6,-12*e-6),(6,-12*e-6)))
print('c1^2-c2 =',s.expand(dot(c1,c1)-dot(L1,L2)))
print('4c2-c1^2 =',s.expand(4*dot(L1,L2)-dot(c1,c1)))

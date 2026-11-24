import sympy as s
e=s.symbols('e', nonnegative=True)
def dot(a,b):
    x,y=a; u,v=b
    return s.expand(-e*x*u+x*v+y*u)
H=(1,3*e+1); P=(4,12*e+3)
L1=(5,-1); L2=(-1,12*e+5)
A=(1,-2*e-1)
for name,D in [('L1',L1),('L2',L2),('A',A)]:
    print(name,'H:',dot(D,H),'P:',dot(D,P),'square:',dot(D,D))
print('H^2',dot(H,H),'P^2',dot(P,P))
print('c2',dot(L1,L2))

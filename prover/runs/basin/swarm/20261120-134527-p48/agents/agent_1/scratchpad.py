import sympy as s

e=s.symbols('e', integer=True, nonnegative=True)
def dot(D,G):
    a,b=D; c,d=G
    return s.expand(-e*a*c+a*d+b*c)
H=(1,3*e+1); P=(4,12*e+3)
A=(5,-1); B=(-1,12*e+5)
c1=(4,12*e+4)
c2=dot(A,B)
assert s.expand(dot(H,H)-(5*e+2))==0
assert s.expand(c2-(65*e+26))==0
assert s.expand(dot(c1,c1)-(80*e+32))==0
assert s.expand(dot(c1,P)-(80*e+28))==0
assert s.expand(dot(A,P)-(40*e+11))==0
assert s.expand(dot(B,P)-(40*e+17))==0
assert s.expand(dot(c1,c1)-c2-(15*e+6))==0
assert s.expand(4*c2-dot(c1,c1)-(180*e+72))==0
print('Verified intersection identities:')
for label,val in [('H^2',dot(H,H)),('c2',c2),('c1^2',dot(c1,c1)),('c1.P',dot(c1,P)),('A.P',dot(A,P)),('B.P',dot(B,P))]:
    print(label,'=',val)

# Wirtinger calculation: f=(sum |v_i|^2)^(-1).
z1,z2,w1,w2=s.symbols('z1 z2 w1 w2')
r=s.symbols('r',positive=True)
f=1/(z1*w1+z2*w2)
levi=s.Matrix(2,2,lambda i,j:s.diff(f,[z1,z2][i],[w1,w2][j]))
levi_axis=s.simplify(levi.subs({z1:r,w1:r,z2:0,w2:0}))
assert levi_axis==s.diag(r**-4,-r**-4)
print('Vertical Levi at (r,0):',levi_axis)
# Positive mean curvature on the two-dimensional base implies at least
# one positive horizontal eigenvalue, not two.
t=s.symbols('t',positive=True)
M=s.diag(3*t,-t)
assert s.trace(M)>0
assert M.det()<0
print('Positive trace does not imply positive definite:',M)

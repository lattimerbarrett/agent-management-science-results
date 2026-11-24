import sympy as s

e=s.symbols('e', integer=True, nonnegative=True)
def dot(a,b):
    x,y=a; u,v=b
    return s.expand(-e*x*u+x*v+y*u)
H=(1,3*e+1); P=(4,12*e+3)
A=(5,-1); B=(-1,12*e+5); c1=(4,12*e+4)
h2=dot(H,H); c2=dot(A,B)
assert s.simplify(h2-(5*e+2))==0
assert s.simplify(c2-13*h2)==0
assert s.simplify(dot(c1,c1)-16*h2)==0
assert s.simplify(dot(c1,P)/2-dot(A,P)-3)==0
assert s.simplify(dot(B,P)-dot(c1,P)/2-3)==0
print('H^2 =',h2,'c1^2 =',dot(c1,c1),'c2 =',c2)
print('slopes:',dot(A,P),dot(c1,P)/2,dot(B,P))
D=(3,-6*e-3)
assert dot(D,H)==0
assert s.simplify(dot(D,D)+9*h2)==0
print('D.H =',dot(D,H),'D^2 =',dot(D,D))
# Check local inverse-norm Levi for a Hermitian-positive normal bundle.
z1,z2,w1,w2=s.symbols('z1 z2 w1 w2', real=True)
# At z=0 and w=(r,0), diagonal curvature lambda_1,lambda_2.
l1,l2,r=s.symbols('lambda1 lambda2 r', positive=True)
# Wirtinger Hessian of 1/|w|^2 has eigenvalues +1/r^4, -1/r^4;
# horizontal entries lambda_i/r^2 for norm exp(-lambda_i|z_i|^2).
x,y,u,v=s.symbols('x y u v',real=True)
f=1/(x*x+y*y+u*u+v*v)
M=s.Matrix([[(s.diff(f,x,2)+s.diff(f,y,2))/4,0],[0,(s.diff(f,u,2)+s.diff(f,v,2))/4]])
M=M.subs({x:r,y:0,u:0,v:0})
assert M==s.diag(r**-4,-r**-4)
print('vertical inverse-norm Levi:',M)
print('Griffiths-positive model full Levi:',s.diag(l1/r**2,l2/r**2,r**-4,-r**-4))
# An explicit infinite family of nonzero weight cohomology groups for U_0.
k=s.symbols('k', integer=True, nonnegative=True)
m=12*e+8+k
a=s.expand(5*m-6)
b=s.expand(12*e+6-m)
assert s.simplify(b+k+2)==0
assert a == 60*e+5*k+34
# H^1(P^1,O(b)) has dimension -b-1=k+1.
assert s.simplify(-b-1-(k+1))==0
print('For m=12e+8+k, a=',a,'b=',b,', h^1 lower bound=',-b-1)
assert s.simplify(dot(A,P)-(40*e+11))==0
assert s.simplify(dot(B,P)-(40*e+17))==0
print('Both split summands have strictly positive P-degree for every e>=0.')

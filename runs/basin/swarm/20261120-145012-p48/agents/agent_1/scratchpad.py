import sympy as sp

e=sp.symbols('e', nonnegative=True, integer=True)
def dot(D,F):
    a,b=D; c,d=F
    return sp.expand(-e*a*c+a*d+b*c)
def add(D,F): return tuple(sp.expand(x+y) for x,y in zip(D,F))
def scale(k,D): return tuple(sp.expand(k*x) for x in D)
S=(1,0); f=(0,1)
H=(1,3*e+1); P=(4,12*e+3)
A=(5,-1); B=(-1,12*e+5)
c1=add(A,B)
checks={
 'c1=4H': c1==scale(4,H),
 'H squared': sp.simplify(dot(H,H)-(5*e+2))==0,
 'c2': sp.simplify(dot(A,B)-(65*e+26))==0,
 'discriminant': sp.simplify(4*dot(A,B)-dot(c1,c1)-(180*e+72))==0,
 'P ample inequality': sp.simplify(P[1]-e*P[0]-(8*e+3))==0,
 'slope': sp.simplify(dot(c1,P)/2-(40*e+14))==0,
 'A slope gap': sp.simplify(dot(c1,P)/2-dot(A,P)-3)==0,
}
for name,passed in checks.items():
    assert passed, name
    print('PASS:',name)
# Complex Hessian in the two fibre variables of 1/(|v1|^2+|v2|^2).
z1,z2,w1,w2=sp.symbols('z1 z2 w1 w2')
r=z1*w1+z2*w2
Levi=sp.Matrix(2,2,lambda a,b:sp.diff(1/r,[z1,z2][a],[w1,w2][b]))
t=sp.symbols('t', positive=True)
at=Levi.subs({z1:t,w1:t,z2:0,w2:0})
assert at==sp.diag(t**-4,-t**-4)
print('PASS: vertical Levi eigenvalues at (t,0):',list(at.diagonal()))
# Horizontal Hessian in Chern-normal coordinates at a point, evaluated
# on a fibre vector (t,0).  The metric coefficient has expansion
# 1 - sum R_ab z_a conjugate(z_b), so 1/||v||^2 has Hessian R/t^2.
a,b,c,d=sp.symbols('a b c d', real=True)
u1,u2,v1,v2=sp.symbols('u1 u2 v1 v2')
R=sp.Matrix([[a,c+sp.I*d],[c-sp.I*d,b]])
s=t*t*(1-(sp.Matrix([[u1,u2]])*R*sp.Matrix([v1,v2]))[0])
LH=sp.Matrix(2,2,lambda k,l:sp.diff(1/s,[u1,u2][k],[v1,v2][l]))
LH=LH.subs({u1:0,u2:0,v1:0,v2:0})
assert sp.simplify(LH-R/t**2)==sp.zeros(2)
assert sp.trace(R)==a+b
print('PASS: horizontal Levi block is curvature block / t^2')
print('Positive curvature trace forces at least one positive horizontal eigenvalue.')

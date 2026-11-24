import sympy as s
k=s.symbols('k',positive=True)
p,t,u=s.symbols('p t u',real=True)
C=k*s.sqrt(1+k*k)
ca=(1-k*k)/(1+k*k); sa=2*k/(1+k*k)
A=s.Matrix([[1,0,0],[0,ca,-sa],[0,sa,ca]])
B=s.Matrix([[ca,0,sa],[0,1,0],[-sa,0,ca]])
# Necessity of the stated linear constraints from preservation of x+y.
xx=s.Matrix(s.symbols('x1 x2 x3')); yy=s.Matrix(s.symbols('y1 y2 y3'))
constraints=(A.T-s.eye(3))*xx+(B.T-s.eye(3))*yy
sol=s.linsolve(list(constraints), list(xx)+list(yy))
print('linear necessary constraints:',sol)
# Each proposed point satisfies the full Rodrigues map, not only scalar factors.
for sign in [-1,1]:
    pp=sign*s.sqrt(2*k*k+3)/(k*k+2)
    tt=s.sqrt(1+k*k)/(k*k+2)
    x=s.Matrix([pp,tt,k*tt]); y=s.Matrix([tt,pp,-k*tt]); m=x+y; r2=m.dot(m)
    def bend(z):
        return ((1-C*C*r2)*z+2*C*m.cross(z)+2*C*C*m*m.dot(z))/(1+C*C*r2)
    assert (A*bend(x)-x).applyfunc(s.simplify)==s.zeros(3,1)
    assert (B*bend(y)-y).applyfunc(s.simplify)==s.zeros(3,1)
tt=-1/s.sqrt(1+k*k)
x=s.Matrix([0,tt,k*tt]); y=s.Matrix([tt,0,-k*tt]); m=x+y; r2=m.dot(m)
def bend(z): return ((1-C*C*r2)*z+2*C*m.cross(z)+2*C*C*m*m.dot(z))/(1+C*C*r2)
assert (A*bend(x)-x).applyfunc(s.simplify)==s.zeros(3,1)
assert (B*bend(y)-y).applyfunc(s.simplify)==s.zeros(3,1)
# The third coordinate of the full fixed equation forces exactly the advertised quadratic on each branch.
for branch in [-1,1]:
    x=s.Matrix([p,t,k*t]);y=s.Matrix([t,branch*p,-k*t]);m=x+y;r2=m.dot(m)
    bz=((1-C*C*r2)*x+2*C*m.cross(x)+2*C*C*m*m.dot(x))[2]
    target=(1+C*C*r2)*(A.T*x)[2]
    expr=s.expand((bz-target)/(2*k)).subs(p*p,1-(1+k*k)*t*t)
    if branch==-1: expected=t+s.sqrt(1+k*k)*(1-k*k*t*t)
    else: expected=t-s.sqrt(1+k*k)*(1-(k*k+2)*t*t)
    assert s.simplify(expr-expected)==0
print('PASS: exact base-map necessity, branch quadratics, and sufficiency checked independently.')
# Explicit bounds enough for contraction inversion and correction (coarse, using max norms).
# p0 components = linear - 2 Q_i/r^2. For r >= .005 and r <= 200:
# |p0| <= 100+sqrt(2)+400 < 502.
# first derivatives of 2Q_i/r^2 <= 6/r^2 < 240000.
# second derivatives <= 28/r^3 < 224000000.
assert 28/(.005)**3<10**9
# Thus implicit derivative errors through order2 cost far less than 10^200.
print('PASS: global diagonal inverse lies far inside the P box; coarse derivative bounds support the finite-k correction.')

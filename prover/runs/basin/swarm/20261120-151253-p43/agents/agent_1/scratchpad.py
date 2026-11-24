import sympy as s

x1,x2,x3,y1,y2,y3,lam,mu = s.symbols('x1 x2 x3 y1 y2 y3 lam mu', real=True)
x=s.Matrix([x1,x2,x3]); y=s.Matrix([y1,y2,y3])
f=x1*y1+x2*(y3-1)+y2*(x3-1)
gx=s.Matrix([s.diff(f,z) for z in x]); gy=s.Matrix([s.diff(f,z) for z in y])
A=s.Matrix([[1,0,0],[0,0,1],[0,1,0]])
e=s.Matrix([0,1,0])
assert gx==A*y-e and gy==A*x-e
assert A.T*A==s.eye(3)
X=gx.cross(x).col_join(gy.cross(y))
assert s.expand(x.dot(X[:3,0]))==0
assert s.expand(y.dot(X[3:,0]))==0

# At a critical point gx=lam*x, gy=mu*y.
eq=list(gx-lam*x)+list(gy-mu*y)
# If x1 != 0, equations 0 and 3 imply lam*mu=1.
assert s.expand(mu*eq[0]+eq[3]-(1-lam*mu)*x1)==0
# Equations 2 and 4 then imply -1=0, a contradiction.
assert s.expand(mu*eq[2]+eq[4]-((1-lam*mu)*x3-1))==0
# If x1=0, eq[0] implies y1=0.
assert eq[0].subs(x1,0)==y1

# With x1=y1=0, criticality is equivalent to the two planar
# tangent derivatives below, plus unit-circle constraints.
planar=[x3*(y3-1)-x2*y2, y3*(x3-1)-x2*y2,
        x2*x2+x3*x3-1, y2*y2+y3*y3-1]
# Their difference forces x3=y3.
assert s.expand(planar[0]-planar[1])==y3-x3
z,u,v=s.symbols('z u v',real=True)
reduced=[s.expand(p.subs({x3:z,y3:z,x2:u,y2:v})) for p in planar]
# Equal radii imply v=u or v=-u. Check each branch exactly.
expected=[]
for sign in [1,-1]:
    polys=[s.expand(p.subs(v,sign*u)) for p in reduced]
    sol=s.solve(polys,[u,z],dict=True)
    for d in sol:
        expected.append((s.S(0),d[u],d[z],s.S(0),sign*d[u],d[z]))
points=set(expected)
assert points=={
    (0,0,1,0,0,1),
    (0,s.sqrt(3)/2,-s.Rational(1,2),0,s.sqrt(3)/2,-s.Rational(1,2)),
    (0,-s.sqrt(3)/2,-s.Rational(1,2),0,-s.sqrt(3)/2,-s.Rational(1,2))}
variables=list(x)+list(y)
for p in points:
    sub=dict(zip(variables,p))
    assert X.subs(sub)==s.zeros(6,1)
    assert s.simplify((x.dot(x)-1).subs(sub))==0
    assert s.simplify((y.dot(y)-1).subs(sub))==0
print('All critical points (exhaustive algebraic solution):')
for p in sorted(points,key=str): print(p,'H =',s.simplify(f.subs(dict(zip(variables,p)))))

# The ambient vector field is 3-Lipschitz on B^3 x B^3:
# diagonal derivative blocks have norm <=2, off-diagonal <=1.
# The block estimate reduces to the norm of this symmetric matrix.
B=s.Matrix([[2,1],[1,2]])
assert set(B.eigenvals())=={1,3}
assert 3 < 2*s.pi
print('Lipschitz constant <= 3 < 2*pi; the period bound excludes nonconstant period-one orbits.')

# Local constrained Hessian at the north/north degenerate point:
a,b,c,d=s.symbols('a b c d',real=True)
# Taylor terms up to total degree three in local tangent coordinates.
local=a*c + b*(-(c*c+d*d)/2) + d*(-(a*a+b*b)/2)
Hess=s.hessian(local,[a,b,c,d]).subs({a:0,b:0,c:0,d:0})
assert Hess.rank()==2
print('Rank of constrained Hessian at north/north:',Hess.rank())

# Check the two remaining critical points are strict nondegenerate extrema.
ambient_hessian=s.hessian(f,variables)
for sign in [-1,1]:
    u=sign*s.sqrt(3)/2; z=-s.Rational(1,2)
    p=s.Matrix([0,u,z]); q=p
    tangent=s.Matrix([[1,0],[0,z],[0,-u]])
    T=s.diag(tangent,tangent)
    sub=dict(zip(variables,list(p)+list(q)))
    multiplier=s.simplify(gx.subs(sub).dot(p))
    L=ambient_hessian-s.diag(multiplier*s.eye(3),multiplier*s.eye(3))
    constrained=s.simplify(T.T*L*T)
    eigs=list(constrained.eigenvals())
    assert all(s.simplify(sign*ev)>0 for ev in eigs)
    print('Extremum sign',sign,'constrained Hessian eigenvalues:',eigs)


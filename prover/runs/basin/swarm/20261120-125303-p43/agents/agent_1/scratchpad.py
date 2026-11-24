import sympy as s

# Exact classification of critical points of f(x,y)=x.y+x_3+y_1.
l,m=s.symbols('l m',real=True)
d=l*m-1
X=s.Matrix([1,0,m])/d
Y=s.Matrix([l,0,1])/d
e1=s.Matrix([1,0,0]); e3=s.Matrix([0,0,1])
assert s.simplify(Y+e3-l*X)==s.zeros(3,1)
assert s.simplify(X+e1-m*Y)==s.zeros(3,1)
P=s.expand(d*d-(1+m*m)); Q=s.expand(d*d-(1+l*l))
assert s.factor(P-Q)==(l-m)*(l+m)
# m=l and m=-l exhaust real solutions.
pplus=s.factor(P.subs(m,l)); pminus=s.factor(P.subs(m,-l))
assert pplus==l*l*(l*l-3)
assert pminus==l*l*(l*l+1)
solplus=s.solve(pplus,l)
solminus=s.solve(pminus,l)
assert set(solplus)=={0,-s.sqrt(3),s.sqrt(3)}
assert solminus==[0]

critical=[]
for a in solplus:
    xx=s.simplify(X.subs({l:a,m:a}))
    yy=s.simplify(Y.subs({l:a,m:a}))
    assert s.simplify(xx.dot(xx))==1
    assert s.simplify(yy.dot(yy))==1
    assert s.simplify((yy+e3).cross(xx))==s.zeros(3,1)
    assert s.simplify((xx+e1).cross(yy))==s.zeros(3,1)
    value=s.simplify(xx.dot(yy)+xx[2]+yy[0])
    critical.append((tuple(xx),tuple(yy),value))
assert len(critical)==3
print('Exactly three critical points, listed as (x,y,f):')
for c in critical:print(c)

# Ambient Hamiltonian vector field.
a,b,c,u,v,w=s.symbols('a b c u v w',real=True)
x=s.Matrix([a,b,c]); y=s.Matrix([u,v,w])
V=(y+e3).cross(x).col_join((x+e1).cross(y))
DV=V.jacobian([a,b,c,u,v,w])
# On B^3 x B^3, its derivative has block norm bounds [[2,1],[1,2]].
# Verify each block is the claimed cross-product operator.
def crossmat(z):
    return s.Matrix([[0,-z[2],z[1]],[z[2],0,-z[0]],[-z[1],z[0],0]])
assert DV[:3,:3]==crossmat(y+e3)
assert DV[:3,3:]==-crossmat(x)
assert DV[3:,:3]==-crossmat(y)
assert DV[3:,3:]==crossmat(x+e1)
B=s.Matrix([[2,1],[1,2]])
assert B.eigenvals()=={3:1,1:1}
# Therefore V is 3-Lipschitz, and V/10 is 3/10-Lipschitz.
# Wirtinger's inequality rules out period 1 whenever L<2*pi.
assert s.Rational(3,10)<2*s.pi
print('All four derivative blocks checked exactly; ambient Lipschitz bound is 3.')
print('For H=f/10, L=3/10<2*pi: the period inequality excludes nonconstant 1-periodic trajectories.')

# Check degeneracy at the third critical point, using local sphere charts.
# Near x=-e1 and y=-e3 use x=(-sqrt(1-p^2-q^2),p,q)
# and y=(r,s,-sqrt(1-r^2-s^2)).
p,q,r,t=s.symbols('p q r t',real=True)
xc=s.Matrix([-s.sqrt(1-p*p-q*q),p,q])
yc=s.Matrix([r,t,-s.sqrt(1-r*r-t*t)])
fc=xc.dot(yc)+xc[2]+yc[0]
Hess=s.hessian(fc,(p,q,r,t)).subs({p:0,q:0,r:0,t:0})
assert Hess.rank()==2
print('Hessian at the critical point of value zero has rank',Hess.rank())

print('Ambient linearized eigenvalues at extrema:')
for xx,yy,value in critical[1:]:
    mat=DV.subs(dict(zip((a,b,c,u,v,w),xx+yy)))
    print(value,s.factor(mat.charpoly().as_expr(),extension=s.sqrt(3)))

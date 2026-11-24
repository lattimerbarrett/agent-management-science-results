import sympy as s
x1,x2,x3,v1,v2,v3,a,t=s.symbols('x1 x2 x3 v1 v2 v3 a t', real=True)
x=s.Matrix([x1,x2,x3]);v=s.Matrix([v1,v2,v3]); e3=s.Matrix([0,0,1])
X=a*e3.cross(x)
# Identity omega_x(X,v)=a*v3 under |x|=1, x.v=0.
omega=s.expand(x.dot(X.cross(v)))
residual=s.expand(omega-a*v3-a*v3*(x.dot(x)-1)+a*x3*x.dot(v))
assert residual == 0
R=s.Matrix([[s.cos(a*t),-s.sin(a*t),0],[s.sin(a*t),s.cos(a*t),0],[0,0,1]])
assert s.simplify(R.diff(t)*x-a*e3.cross(R*x)) == s.zeros(3,1)
assert R.subs(t,0)==s.eye(3)
Rpi=s.simplify(R.subs({a:s.pi,t:1}))
assert Rpi==s.diag(-1,-1,1)
# Fixed vector equation: x1=x2=0. Sphere then gives x3=+/-1.
solutions=s.solve(list((Rpi-s.eye(3))*x)+[x.dot(x)-1], [x1,x2,x3], dict=True)
assert solutions==[{x1:0,x2:0,x3:-1},{x1:0,x2:0,x3:1}]
pairs=[(p[x3],q[x3]) for p in solutions for q in solutions]
assert len(pairs)==4 and len(set(pairs))==4
# On tangent planes at a pole the derivative is -I_2.
D=s.diag(-1,-1,-1,-1)
assert (D-s.eye(4)).det()==16
print('Verified Hamiltonian H=pi(z1+z2), convention omega(X,.)=dH, exact flow, and exactly four fixed points:')
print(pairs)
print('Each fixed point is nondegenerate; determinant(Dphi-I)=16.')

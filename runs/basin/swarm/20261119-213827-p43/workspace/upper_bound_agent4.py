import sympy as s
x, y, z, u, v, w = s.symbols("x y z u v w", real=True)
a, b, c = s.symbols("a b c", real=True)
p=s.Matrix([x,y,z]); eta=s.Matrix([a,b,c]); e3=s.Matrix([0,0,1])
X=e3.cross(p)
# omega(X, eta)-dz(eta) vanishes when |p|=1 and eta tangent.
identity=s.expand(p.dot(X.cross(eta))-c - (c*(p.dot(p)-1)-z*p.dot(eta)))
assert identity == 0
# Time t flow of pi*height; differentiating verifies ODE.
t=s.symbols("t", real=True)
R=s.Matrix([[s.cos(s.pi*t),-s.sin(s.pi*t),0],[s.sin(s.pi*t),s.cos(s.pi*t),0],[0,0,1]])
assert s.simplify(s.diff(R*p,t)-s.pi*e3.cross(R*p)) == s.zeros(3,1)
R1=s.simplify(R.subs(t,1))
assert R1 == s.diag(-1,-1,1)
# Solve fixed equations on both spheres exactly.
q=s.Matrix([u,v,w])
eqs=list((R1-s.eye(3))*p)+list((R1-s.eye(3))*q)+[p.dot(p)-1,q.dot(q)-1]
solutions=s.solve(eqs,[x,y,z,u,v,w],dict=True)
assert len(solutions)==4
assert {(r[z],r[w]) for r in solutions}=={(-1,-1),(-1,1),(1,-1),(1,1)}
for r in solutions:
    assert all(s.simplify(f.subs(r))==0 for f in eqs)
print("Hamiltonian identity verified; exact time-one rotation verified; fixed points:")
for r in solutions: print(tuple(r[a] for a in [x,y,z,u,v,w]))

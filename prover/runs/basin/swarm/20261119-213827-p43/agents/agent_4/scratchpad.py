import sympy as s
from pathlib import Path
code = '''import sympy as s
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
'''
Path('workspace/upper_bound_agent4.py').write_text(code)
exec(code)
cone_code='''import sympy as s
r=s.symbols("r", positive=True)
rho=s.exp(-1/r**2)
assert s.simplify(s.diff(rho,r)-2*rho/r**3)==0
# Every radial derivative is a Laurent polynomial times exp(-1/r^2).
P=s.Integer(1)
D=rho
for n in range(13):
    assert s.expand(D/rho-P)==0
    for term in s.Add.make_args(s.expand(P)):
        coeff,power=term.as_coeff_exponent(r)
        assert power.is_integer
        assert s.limit(r**power*rho,r,0,dir="+")==0
    P=s.expand(s.diff(P,r)+2*P/r**3)
    D=s.diff(D,r).expand()
# Full Euclidean gradient norm identity for a radially constant angular function.
x=s.Matrix(s.symbols("x0:4",real=True)); dg=s.Matrix(s.symbols("d0:4",real=True))
a,b,g=s.symbols("a b g",real=True)
D=a*g*x/r+b*dg
rhs=a*a*g*g*x.dot(x)/r**2+b*b*dg.dot(dg)+2*a*b*g*x.dot(dg)/r
assert s.expand(D.dot(D)-rhs)==0
# On |x|=r and x.dot(dg)=0, this is a^2*g^2+b^2*|dg|^2.
print("Flatness derivative recurrence verified through order 12; exact gradient norm identity verified.")
'''
Path('workspace/cone_agent4.py').write_text(cone_code)
exec(cone_code)

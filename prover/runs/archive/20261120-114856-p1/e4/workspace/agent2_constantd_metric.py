import sympy as S
from pathlib import Path
x=S.symbols('x');nodes=list(map(S.Rational,[-8,-7,-4,-1,1,4,7,8]))
p=x**4-65*x*x+424;C=S.Integer(360)**2;P=S.expand(p*p-C);tau=x**3-S.Rational(65,2)*x
pp=S.diff(p,x)
# Conditional +/- group weights are tau/p' and each group sums to one.
for sign in [-1,1]:
 assert sum(tau.subs(x,z)/pp.subs(x,z) for z in nodes if p.subs(x,z)==sign*360)==1
Hnode=S.Matrix(3,3,lambda i,j:sum(S.sign(p.subs(x,z))*z**(i+j)/(pp.subs(x,z)*tau.subs(x,z)) for z in nodes))
# Residue theorem rewrites the signed Fisher metric in Dirichlet-root form.
Pinv=S.invert(P,tau,x)
Hroot=S.Matrix(3,3,lambda i,j:-720*S.Poly(S.rem(x**(i+j)*Pinv,tau,x),x).nth(2))
assert Hnode==Hroot
assert Hnode.det()!=0
print('Exact constant-d signed Fisher = diagonal Dirichlet/Staeckel metric: PASS')
print(Hnode)

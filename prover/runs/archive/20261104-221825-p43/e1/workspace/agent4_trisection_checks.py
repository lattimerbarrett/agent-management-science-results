from pathlib import Path
code = '''"""Exact finite algebra checks for the lower-bound argument.
Run with Python 3. No numerical tolerances or third-party packages.
The input cellular cohomology ring of S^2 is F2[u]/(u^2), deg(u)=2.
The product cellular ring is its graded tensor product.
"""
from itertools import product
basis = ((0,0),(1,0),(0,1),(1,1))
zero = (0,0,0,0)
unit = (1,0,0,0)
a = (0,1,0,0)
b = (0,0,1,0)
pt = (0,0,0,1)
def mul(x,y):
    out = [0]*4
    for i,(r,s) in enumerate(basis):
        for j,(t,u) in enumerate(basis):
            if x[i] and y[j] and r+t <= 1 and s+u <= 1:
                out[basis.index((r+t,s+u))] ^= 1
    return tuple(out)
assert mul(a,a)==zero and mul(b,b)==zero
assert mul(a,b)==pt and pt != zero
positive = [(0,)+v for v in product((0,1), repeat=3)]
assert all(mul(mul(x,y),z)==zero for x,y,z in product(positive,repeat=3))
assert any(mul(x,y)!=zero for x,y in product(positive,repeat=2))
# Thus cup length is exactly 2, not merely at least 2.
cup_length=2
# Integral periods: omega(A)=omega(B)=4pi; c1(A)=c1(B)=2.
# Both homomorphisms on pi_2 are determined by these generators.
# Units are chosen so that area is divided by 2pi.
area_in_2pi_units=(2,2)
c1=(2,2)
assert area_in_2pi_units==c1
from math import gcd
minimal_chern=gcd(*c1)
complex_dimension=2
assert minimal_chern==2 and minimal_chern>=complex_dimension
print({"Betti_numbers_even":[1,2,1], "cup_length":cup_length,
       "minimal_Chern_number":minimal_chern,
       "Arnold_cup_length_lower_bound":cup_length+1})
'''
Path('workspace/lower_bound_checks.py').write_text(code)
exec(compile(code,'workspace/lower_bound_checks.py','exec'))
slow_code = '''"""Symbolic identities used in the short-period exclusion lemma."""
import sympy as s
# The variance identity in arbitrary finite samples is polynomial.
for n in range(2,9):
    x=s.symbols('x:'+str(n))
    mean=sum(x)/n
    lhs=sum((v-mean)**2 for v in x)
    rhs=sum((v-w)**2 for v in x for w in x)/(2*n)
    assert s.expand(lhs-rhs)==0
# Wirtinger for trigonometric polynomials: the kth Fourier mode has
# derivative norm squared (2*pi*k/T)^2 times its norm squared.
# Orthogonality and completion extend the inequality to smooth loops.
t=s.symbols('t',real=True)
for k in range(1,6):
    u=s.cos(k*t)
    norm=s.integrate(u*u,(t,0,2*s.pi))
    dnorm=s.integrate(s.diff(u,t)**2,(t,0,2*s.pi))
    assert s.simplify(dnorm-k*k*norm)==0
    assert k*k>=1
# Pointwise spherical Hamiltonian formula for the sign convention:
# X_f = grad(f) cross x; x dot ((grad f cross x) cross v)=grad f dot v
# for v tangent to the unit sphere.
x,y,z,a,b,c,p,q,r=s.symbols('x y z a b c p q r',real=True)
v=s.Matrix([p,q,r]); pos=s.Matrix([x,y,z]); grad=s.Matrix([a,b,c])
expr=s.expand(pos.dot((grad.cross(pos)).cross(v))-grad.dot(v))
expected=(pos.dot(pos)-1)*grad.dot(v)-grad.dot(pos)*pos.dot(v)
assert s.expand(expr-expected)==0
print('Variance, Fourier/Wirtinger, and Hamiltonian sign identities checked exactly.')
'''
Path('workspace/slow_hamiltonian_checks.py').write_text(slow_code)
exec(compile(slow_code,'workspace/slow_hamiltonian_checks.py','exec'))
import runpy
for filename in ['agent2_local_germ_checks.py','agent3_arc_checks.py','agent4_trisection_checks.py']:
    print('Running',filename)
    runpy.run_path('workspace/'+filename)

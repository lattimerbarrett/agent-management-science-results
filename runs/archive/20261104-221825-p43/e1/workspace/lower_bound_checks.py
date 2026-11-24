"""Exact finite algebra checks for the lower-bound argument.
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

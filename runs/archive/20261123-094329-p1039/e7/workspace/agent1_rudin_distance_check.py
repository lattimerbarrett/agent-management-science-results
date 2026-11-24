import sympy as s
c=s.symbols("c",real=True)
g=2+c
# For p=(4,0), |z-p_z| >= ||z|-4| and |z|=g^2.
D=s.expand((g*g-4)**2+g*g*(1-c*c)*(1+4*c*c))
expected=-4*c**6-16*c**5-12*c**4+20*c**3+29*c**2+4*c+4
assert s.expand(D-expected)==0
# Exact Sturm root count: no zeros, and positive at 0, imply D>3 on [-1,1].
assert s.Poly(D-3,c).count_roots(-1,1)==0
assert (D-3).subs(c,0)>0
print("Exact Sturm certificate: dist((4,0), Rudin KB)^2 > 3.")
print("Thus every sufficiently small tubular neighborhood excludes p.")
print("No Oka/non-Oka implication is asserted by this computation.")

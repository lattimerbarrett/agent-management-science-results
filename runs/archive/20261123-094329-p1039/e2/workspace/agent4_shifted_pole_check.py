import sympy as s
u,e=s.symbols('u e',positive=True)
A=e**2-(u-1)**2
D=lambda f:2*u*s.diff(f,u)
N=2*(u-(1-e**2))**2+2*e**2*(1-e**2)
assert s.simplify(D(D(s.log(A)/2))+2*u*N/A**2)==0
# 0<e<1 implies N>0; on 1-e<u<1+e, A>0.
assert s.expand(N)==s.expand(2*u*u+(4*e*e-4)*u+2-2*e*e)
# Exact shifted-pole finite geometric identity, with error tending to 0
# whenever |a|<|z-a|.
z,a=s.symbols('z a')
for m in range(1,12):
    partial=sum((-a)**k/(z-a)**(k+1) for k in range(m))
    remainder=(-a)**m/(z*(z-a)**m)
    assert s.factor(1/z-partial-remainder)==0
print('Verified solid-torus log-concavity identity and shifted-pole geometric-series formula.')

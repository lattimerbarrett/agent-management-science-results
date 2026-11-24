import sympy as s
n,r=s.symbols("n r",positive=True)
a=(n-2)/2
ld=-2*a*r/(1+r*r)
lap_over_U=s.factor(s.diff(ld,r)+ld**2+(n-1)*ld/r)
assert s.simplify(lap_over_U+n*(n-2)/(1+r*r)**2)==0
c=(n-2)/(4*(n-1))
psi_lap_ratio=s.factor(a*(a+1)/r**2-(n-1)*a/r**2)
R=s.factor(-psi_lap_ratio*r**2/c)
assert s.simplify(R-(n-1)*(n-2))==0
assert s.simplify(c*R-(n-2)**2/4)==0
q=2*n/(n-2)
assert s.simplify(n*(n-2)/q-(n-2)**2/2)==0
print("Bubble PDE, cylinder scalar/eigenvalue, radial potential identities passed.")

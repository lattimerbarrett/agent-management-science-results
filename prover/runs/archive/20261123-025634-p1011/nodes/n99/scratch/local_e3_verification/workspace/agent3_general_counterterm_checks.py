"""Exact derivative matching for linear geometry Pohozaev counterterm.
No nonlinear blow-up projection estimate is asserted.
"""
import sympy as s
r,n=s.symbols('r n',positive=True)
H=s.Function('H')(r)
a=(n-2)/2;b=(n-2)/(2*(n-1))
# H(r)=angular integral of boundary graph h(r theta).
g=(n-2)*r**(-n)*(H-r*s.diff(H,r)+r**2/(2*(n-1))*(s.diff(H,r,2)+(n-2)/r*s.diff(H,r)))
L=a*b*r**(-(n-2))*(2*H/r-s.diff(H,r))
assert s.simplify(s.diff(L,r)+a*g)==0
# For harmonic V, P_linear=-a[r Vmean'+(n-2)Vmean].
V=s.Function('V')(r)
P=-a*(r*s.diff(V,r)+(n-2)*V)
# Harmonic hemisphere equation: r Vmean''+(n-1)Vmean'=g.
assert s.simplify(s.diff(P,r)+a*(r*s.diff(V,r,2)+(n-1)*s.diff(V,r)))==0
print('General graph linear Pohozaev/counterterm derivative matching checked exactly.')

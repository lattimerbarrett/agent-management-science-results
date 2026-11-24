import sympy as s
# Ordinary cohomology, with a^2=b^2=0.
a,b=s.symbols('a b')
G=s.groebner([a*a,b*b],a,b)
for p in (a,b,a*b,a*a*b,a*b*b):
 print(str(p),'->',G.reduce(p)[1])
print('Spherical areas are 4*pi*Z; minimal Chern number is 2.')
print('Finite fixed set has H^{>0}=0, so positive-degree classes restrict to zero.')
print('This is the isolation input in strict spectral LS inequalities.')
print('Distinct numerical action selectors alone do not imply distinct geometric orbits: recappings must be included in the cup-length theorem.')
import sympy as s
n=s.symbols('n',integer=True,positive=True)
p=(n+2)/(n-2)
# Kelvin transform v(y)=|y|^(2-n) u(y/|y|^2).
# Laplacian and critical nonlinear term have matching conformal weights.
print('Kelvin critical exponent discrepancy:',s.simplify((2-n)*p-(-n-2)))
# Energy of an ordinary capacity cutoff around the compactification point.
r=s.symbols('r',positive=True)
print('Cutoff energy scale:',r**(n-2))
# Finite-energy lower-order potential is precisely critical Lebesgue class.
print('Potential integrability exponent:',s.simplify((p-1)*n/2))
print('Sobolev exponent:',2*n/(n-2))
print('At n=19 these are:',s.simplify(((p-1)*n/2).subs(n,19)))

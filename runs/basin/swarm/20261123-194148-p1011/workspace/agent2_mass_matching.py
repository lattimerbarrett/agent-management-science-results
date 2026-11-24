import sympy as s
from pathlib import Path
n,k=s.symbols('n k',integer=True,positive=True)
a=(n-2)/2; beta=(n-2)/(2*(n-1))
D=1-k+k*(k+n-3)/(2*(n-1))
assert s.simplify(D-(k-2)*(k-n+1)/(2*(n-1)))==0
A=(n-1-k)*(k-1)
meanpsi=-(n-2)*D/A
Plinear=s.factor(-a*(k-1)*meanpsi)
expected=beta*a*(2-k)
assert s.simplify(Plinear-expected)==0
print('Exact radial geometric Green Pohozaev coefficient:',Plinear)
print('Equals Kelvin ADM rim correction beta*a*(2-k).')
# Kelvin radial Pohozaev algebra.
w,z,R=s.symbols('w z R')
q=-(n-2)*w-R*z
assert s.simplify(a*w*q+q*q/2-(a*R*w*z+R*R*z*z/2))==0
print('Kelvin Pohozaev transformation checked.')

import sympy as s
from pathlib import Path
n,r=s.symbols('n r', positive=True)
k=n-2; N=n-1; alpha=k/(2*N)
U=(1+r*r)**(-k/2)
D=s.diff(U,r)**2/2-k*k*(1+r*r)**(-n)/2
lapU2=s.diff(U*U,r,2)+(N-1)/r*s.diff(U*U,r)
assert s.simplify((D-alpha*lapU2/2)*(1+r*r)**n)==0
print('All-n exact first shape-energy cancellation verified symbolically.')
# Energy tail cubic exponent for highest degree8 in n19:
d=s.symbols('d')
exp=s.expand(3*d+(-2*n)+(n-2))
assert exp.subs({n:19,d:8})==3
print('Third-order energy radial integrand exponent 3d-n-2=',exp,'; n19,d8 => integral O(R^4).')
Path('workspace/agent2_shape_energy_cancellation.py').write_text(Path(__file__).read_text())

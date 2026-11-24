"""Exact checks for the mass contribution in the local critical Pohozaev identity.
This does not prove blow-up compactness: the geometric remainder sign is missing.
"""
import sympy as s
r,a,A,n=s.symbols('r a A n', positive=True)
# Radial harmonic Green model on Euclidean half space.
G=a*r**(2-n)+A
Gp=s.diff(G,r)
# Flux density, excluding the nonlinear term (absent in the Green limit),
# integrated over half-sphere: factor omega_(n-1)/2 omitted.
flux=s.expand(r**(n-1)*((n-2)*G*Gp/2-r*Gp**2/2+r*Gp**2))
expected=-(n-2)**2*a*A/2
assert s.simplify(flux-expected)==0
# Harmonicity in every dimension.
assert s.simplify(s.diff(Gp,r)+(n-1)*Gp/r)==0
# Centered nonlinear bubble has identically zero spherical Pohozaev flux.
eps=s.symbols('eps',positive=True)
a0=(n-2)/2
D=eps**2+r**2
logder=-(n-2)*r/D
F_over_U2=(n-2)**2*eps**2/(2*D**2)
assert s.simplify(a0*logder+r*logder**2/2+r*F_over_U2)==0
# Robin boundary algebra after tangential integration by parts.
b=(n-2)/(2*(n-1))
H,z=s.symbols('H z')
# u^2 coefficient: divergence term, original a*u*normal term,
# plus the normal-gradient contribution. z denotes X dot nu.
coefficient=b*H*(n-1-H*z)/2-a0*b*H+z*b*b*H*H/2
assert s.simplify(coefficient-(b*H/2+z*b*(b-1)*H*H/2))==0
print('Green-model half-sphere Pohozaev flux / omega_(n-1) =',s.factor(flux/2))
# Store reusable verification next to other agents' independent files.
from pathlib import Path
Path('workspace/agent2_mass_flux.txt').write_text(str(s.factor(flux/2))+'\n')
Path('workspace/agent2_pohozaev_checks.py').write_text(Path(__file__).read_text())
print('All symbolic assertions passed. No sharp geometric remainder asserted.')

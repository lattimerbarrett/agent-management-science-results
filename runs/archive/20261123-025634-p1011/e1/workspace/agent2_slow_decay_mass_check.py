from pathlib import Path
import sympy as s
r,a,tau,n=s.symbols('r a tau n',positive=True)
S=r+a*r**(1-tau)
A=s.diff(S,r)**2
B=(S/r)**2
flux=s.simplify(s.expand(A-B-r*s.diff(B,r)))
assert s.simplify(flux-a*a*tau*tau*r**(-2*tau))==0
mass=s.simplify(flux*r**(n-2)/4)
print('Euclidean halfspace radial coordinate change apparent ADM mass:',mass)
print('At tau=1:',s.simplify(mass.subs(tau,1)))
Path('workspace/agent2_slow_decay_mass_check.py').write_text(Path(__file__).read_text())

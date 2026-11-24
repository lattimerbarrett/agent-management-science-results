import sympy as s
from pathlib import Path
n,d=s.symbols('n d',positive=True)
a=(n-2)/2;beta=d+1-n
K=s.factor((n-2)*(1-d+d*(d+n-3)/(2*(n-1))))
assert s.factor(K-(n-2)*(d-2)*beta/(2*(n-1)))==0
meanphi=s.factor(K/(beta*(beta+n-2)))
Pcross=s.factor(-a*(beta+n-2)*meanphi)
assert s.factor(Pcross+(n-2)**2*(d-2)/(4*(n-1)))==0
print('radial graph Robin forcing coefficient:',K)
print('Green correction hemisphere mean / equator area:',meanphi)
print('raw Pohozaev linear coefficient / equator area:',Pcross)
print('example n=10,d=6: exponent',beta.subs({n:10,d:6}),'coefficient',Pcross.subs({n:10,d:6}))
if __file__.endswith('scratchpad.py'):
 Path('workspace/agent1_green_flux_warning.py').write_text(Path(__file__).read_text())

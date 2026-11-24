import sympy as S
from pathlib import Path
v,w=S.symbols('v w',real=True)
for n in range(3,18):
 dv=S.symbols('dv:'+str(n),real=True)
 dw=S.symbols('dw:'+str(n),real=True)
 lhs=sum((v*b+w*a)**2 for a,b in zip(dv,dw))
 rhs=v*v*sum(b*b for b in dw)+sum(a*(a*w*w+2*v*w*b) for a,b in zip(dv,dw))
 assert S.expand(lhs-rhs)==0
# Constant smooth addition under inversion contributes the mass-order factor.
r,A,nn=S.symbols('r A nn',positive=True)
# (r^(2-n)+A)/r^(2-n)=1+A*r^(n-2), then r=1/R.
assert S.simplify((r**(2-nn)+A)/r**(2-nn)-(1+A*r**(nn-2)))==0
print('Ground-state product identity verified for all coordinate dimensions3..17; Green smooth-addition ratio exact symbolically.')
Path('workspace/agent2_cover_mass_checks.py').write_text(Path(__file__).read_text())

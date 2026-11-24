import sympy as S
from pathlib import Path
n,t1,t2,z,c1,c2,t=S.symbols('n t1 t2 z c1 c2 t', positive=True)
# z= squared horizontal separation; t1,t2 positive heights. The direct
# pair kernel is unchanged by common vertical translation.
direct=(z+((t1+t)-(t2+t))**2)**((2-n)/2)
assert S.diff(direct,t)==0
# Image pair contribution, including the two symmetric cross terms.
base=z+(t1+t2+2*t)**2
image=2*c1*c2*base**((2-n)/2)
D=S.diff(image,t).subs(t,0)
expected=-4*(n-2)*c1*c2*(t1+t2)*(z+(t1+t2)**2)**(-n/2)
assert S.simplify(S.powsimp(D-expected,force=True))==0
# Each diagonal self-image term also has a strictly negative derivative.
selfterm=c1**2*(2*(t1+t))**(2-n)
Ds=S.diff(selfterm,t).subs(t,0)
assert S.simplify(Ds+(n-2)*c1**2*2**(2-n)*t1**(1-n))==0
print('Common normal translation derivative: direct=0; image pair=',expected)
print('For every n>2, positive heights and weights make all nonzero image derivatives strictly negative.')
Path('workspace/agent2_neumann_image_force_checks.py').write_text(Path(__file__).read_text())

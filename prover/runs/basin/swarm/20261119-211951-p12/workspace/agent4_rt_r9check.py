from pathlib import Path
from fractions import Fraction as Q
from math import factorial
from functools import lru_cache
from collections import defaultdict
prime=1000000007
# Load only definitions, avoiding any source-copy/output side effects.
src=Path('workspace/agent3_fz25.py').read_text().split('cols=parts(N);')[0]
src=src.replace('N=12; g=25','N=9; g=24')
ns={};exec(src,ns)
Ppoly=ns['P'];A=ns['A'];B=ns['B']
ns2={};exec(Path('workspace/agent2_boundary_functional25.py').read_text().split('# Independent direct string')[0],ns2)
pointed=ns2['pointed'];onepoint=ns2['onepoint']
def mod(x):return x.numerator%prime*pow(x.denominator%prime,-1,prime)%prime
base=Path('workspace/agent3_fz25.py').read_text().split('cols=parts(N);')[0].replace('N=12; g=25','N=9; g=24')
ng={};nr={}
exec(base.replace('(2*g-2 if n==0 else 1)','(48 if n==0 else 1)'),ng)
exec(base.replace('(2*g-2 if n==0 else 1)','(47 if n==0 else 1)'),nr)
for sigma,ai,aj in [((),0,0),((),1,1),((1,),0,1),((1,),1,0),((1,1),0,0)]:
 Ppoly=ng['H'](sigma)
 for extra in [(15,), (7,8), (1,)*15]:
  smooth=0;tail=0
  C1=A if ai==0 else B;C2=A if aj==0 else B
  for p,c in Ppoly.items():
   k=sum(p)
   if k>9:continue
   for e in range(10-k):
    f=9-k-e
    smooth=(smooth+mod(c*C1[e]*C2[f])*pointed(tuple(sorted(p+extra)),e,f))%prime
  s=sigma.count(1)
  for m in range(s+1):
   sf=Q((-1)**(m+ai+aj)*factorial(s),factorial(s-m))
   sigmar=tuple(list(sigma)[m:])
   hc=nr['H'](sigmar)
   for p,c in hc.items():
    d=9-sum(p)
    if d<1:continue
    ec=-A[d] if (m+ai+aj)%2==0 else B[d]
    tail=(tail+mod(c*sf*ec)*onepoint(tuple(sorted(p+extra)),d-1))%prime
  print('r9 sigma=',sigma,'a=',(ai,aj),'test=',extra,'open=',smooth,'tail=',tail,'sum=',(smooth+tail)%prime)
  assert (smooth+tail)%prime==0
print('All fifteen minimal-r9 fullRT correction checks passed.')
if Path(__file__).name=='scratchpad.py':Path('workspace/agent4_rt_r9check.py').write_text(Path(__file__).read_text())

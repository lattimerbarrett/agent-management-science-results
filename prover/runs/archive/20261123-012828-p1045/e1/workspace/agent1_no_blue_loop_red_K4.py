import sympy as S
a,c,L,k,t=S.symbols('a c L k t',real=True)
assert S.expand((k+t*L)**2-a*L**2-2*L - ((t*t-a)*L**2+(2*k*t-2)*L+k*k))==0
mu=S.symbols('mu',positive=True)
# c=2mu-mu² and a<mu² imply t<mu; belowhom gives t>sqrt(a).
assert S.expand(mu-(a+2*mu-mu**2)/2-(mu**2-a)/2)==0
# Numerical tests of exclusion: sample admissible a,b and degrees di>=mu;
# the resulting positive polynomial forbids a four-clique.
import numpy as np
rng=np.random.default_rng(81)
checked=0
for _ in range(10000):
 aa=rng.uniform(0,.25);bb=rng.uniform(aa,.5)
 if np.sqrt(aa)+np.sqrt(bb)>=1:continue
 cc=1-bb;tt=(aa+cc)/2;mm=1-np.sqrt(bb)
 assert np.sqrt(aa)<tt<mm and tt>.25
 dd=rng.uniform(mm,1,4);ll=np.sum(1/(dd-tt))
 assert (tt*tt-aa)*ll*ll+(8*tt-2)*ll+16>0
 checked+=1
print('Exact clique-polynomial algebra and',checked,'admissible sampled exclusions verified.')

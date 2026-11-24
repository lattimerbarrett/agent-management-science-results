import sympy as s,pickle
from pathlib import Path
z,c,d,S,Q,H=s.symbols('z c d S Q H',real=True)
m=S+c-z;f1=d-c*z;f0=-d*z;M2=f1+S*m-Q;M3=f0+S*M2-Q*m
A=s.factor((m*M2-M3)/(M2-m*m));B=s.factor(-M2-A*m)
HH=s.factor(H+B*d-z*(A*d+B*c));ZZ=s.factor((B*d*z-(m+A)*H)/HH)
print('A',A);print('B',B);print('H',HH);print('znew',ZZ)
a=-S-c;d0=s.factor(c*(Q-a*c)/(c-a));b0=s.factor(-a*(Q-a*c)/(c-a));H0=s.factor(H+b0*d0)
assert s.factor((A-a).subs(d,d0))==0
assert s.factor((B-b0).subs(d,d0))==0
assert s.factor((ZZ-z).subs(d,d0))==0
assert s.factor(H0-(H-a*c*(Q-a*c)**2/(c-a)**2))==0
print('All stationarysurface exact identities VERIFIED')
pickle.dump((z,c,d,S,Q,H,A,B,HH,ZZ,d0,b0,H0),open('workspace/critical_cubic_map_agent2.pkl','wb'))
Path('workspace/critical_cubic_map_agent2.py').write_text(Path(__file__).read_text())

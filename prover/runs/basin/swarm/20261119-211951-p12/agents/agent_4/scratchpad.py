from pathlib import Path
from fractions import Fraction as Q
import json
s=Path('workspace/agent2_boundary_functional25.py').read_text().split('# Independent direct string')[0].replace('P=1000000007;h=24','P=1000000007;h=12')
ns={};exec(s,ns);p=ns['P']
fz=json.load(open('workspace/agent3_fz25.json'));cols=fz['columns']
L=[pow(2,len(a),p)*ns['pointed'](tuple(a),0,0)%p if all(i%2==0 for i in a) else 0 for a in cols]
vs=[]
for r in fz['rows']:
 z=sum(Q(c).numerator%p*pow(Q(c).denominator,-1,p)*l for c,l in zip(r,L))%p;vs.append(z)
print('FZ necessaryconsistency nonzero',sum(bool(v) for v in vs),'/',len(vs)); print(vs)

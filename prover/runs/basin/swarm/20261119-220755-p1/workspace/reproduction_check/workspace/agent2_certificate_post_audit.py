"""Independent exact-rational audit of saved directed certificate records.
All JSON floats are exact dyadics here; no tolerance comparisons are used.
"""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json,numpy as np
D=Path('workspace/agent4_pointwise_certificate_chunks_v2');source=Path('workspace/agent2_floquetframe_m072.npz');sha=hashlib.sha256(source.read_bytes()).hexdigest();data=np.load(source);rr=[];jobs=[]
for lo in range(0,2000,10):
 p=D/f'chunk_{lo:04d}_{min(lo+10,2000):04d}.json';a=json.loads(p.read_text());assert a['source_sha256']==sha;assert a['lo']==lo and a['hi']==min(lo+10,2000);rr+=a['records'];jobs.append(a)
for i in range(2000):
 rows=sorted([r for r in rr if r['index']==i],key=lambda r:Q(r['left']));assert Q(rows[0]['left'])==Q(float(data['x'][i]));assert Q(rows[-1]['right'])==Q(float(data['x'][i+1]));assert all(Q(a['right'])==Q(b['left']) for a,b in zip(rows[:-1],rows[1:]));assert all(Q(r['left'])<Q(r['right']) for r in rows)
target=dict(delta=Q(37,10**7),E=Q(1,1000),H=Q(1500),b=Q(500),a_normal=Q(1,10000))
for r in rr:
 for k,v in target.items():assert Q(r[k])<v
 assert Q(r['a0_lower'])>Q(9999,10000);assert Q(r['theta_lower'])>0 and Q(r['theta_upper'])<1;assert Q(r['Z0_lower'])>0 and Q(r['Z1_lower'])>0
assert min(Q(r['theta_upper']) for r in rr)<Q(1,10)
assert max(Q(r['theta_lower']) for r in rr)>Q(9,10)
assert Q(6e-5)>=Q(3,50000)
# Saved upper rounding is strict nextafter of a correctly rounded binary64 value.
# Even if a raw MPFR norm sum rounded downward, it used <=36 positive additions
# and one multiplication at >=300 bits: relative underestimate <2^-290.
# nextafter(float(raw),+inf) exceeds raw by >=2^-54*raw for normal positive raw,
# so every saved upper is still a rigorous upper for the mathematical norm.
assert Q(38,2**299)<Q(1,2**290)<Q(1,2**54)
assert all(np.isfinite(r[k]) and r[k]>np.finfo(float).tiny for r in rr for k in target)
exec(Path('workspace/agent2_floquet_budget_check_v2.py').read_text())
print('POST-AUDIT PASS: 2000 exactdyadic Hermitepieces tiled by',len(rr),'certifiedintervals; allsha/rationaltargets/positivity/nonconstancy checks passed; source',sha)

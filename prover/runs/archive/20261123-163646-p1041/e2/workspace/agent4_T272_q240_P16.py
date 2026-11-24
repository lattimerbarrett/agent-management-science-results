import itertools,json,numpy as np,sys
from pathlib import Path
# Load only functions from our durable checker, not its computation.
s=Path('workspace/agent4_boundary256_orbits.py').read_text();exec(s[:s.index('m=9;mons=')])
mons=[sum(1<<j for j in I) for k in range(4) for I in itertools.combinations(range(9),k)]
vs=[sum(1<<j for j,M in enumerate(mons) if x&M==M) for x in range(512)]
q=[sum((x>>(2*j)&1)*(x>>(2*j+1)&1) for j in range(4))&1 for x in range(512)]
assert sum(q)==240
results=[]
for j in [0,1]:
 t=4-j;P=span([1<<(2*i) for i in range(t)]+([256] if j else []));assert len(P)==16 and all(not q[x] for x in P)
 sol,r=solve([(vs[x],int(x in P)) for x in range(512) if not q[x]],130)
 result={'radical_intersection':j,'solvable':sol is not None}
 if sol is not None:
  h=[(v&sol).bit_count()&1 for v in vs];f=h+[h[x]^q[x] for x in range(512)];assert sum(f)==272 and degree(f)<=3
  S={x for x,b in enumerate(f) if b};unused=[v for v in range(1,1024) if all(x^v not in S for x in S)];result.update({'unused':unused,'support':sorted(S),'h_ANF':[M for i,M in enumerate(mons) if sol>>i&1]})
 print({k:v for k,v in result.items() if k!='support'},flush=True);results.append(result)
Path('workspace/agent4_T272_q240_P16.json').write_text(json.dumps(results))

from sage.all import simplicial_complexes
from itertools import combinations
from pathlib import Path
import time,json,z3
D=[tuple(int(v) for v in f) for f in simplicial_complexes.DunceHat().facets()]
labels=sorted(set(v for f in D for v in f));index={v:i for i,v in enumerate(labels)}
D=[tuple(sorted(index[v] for v in f)) for f in D];n=len(labels)
T=[]
for a,b,c in D:
 for z in [(a,b,c,c+n),(a,b,b+n,c+n),(a,a+n,b+n,c+n)]:T.append(sum(1<<v for v in z))
T=tuple(sorted(T));N=len(T);print('base DH triangles',len(D),'prism tets',N,flush=True)
S=z3.Solver();S.set(timeout=180000);R=[z3.Int('r'+str(i)) for i in range(N)]
S.add(z3.Distinct(R))
for r in R:S.add(r>=0,r<N)
for j,f in enumerate(T):
 for i,g in enumerate(T):
  if i==j:continue
  witnesses=[]
  for h,v in enumerate(T):
   diff=f&~v
   if diff and not diff&(diff-1) and not diff&g:witnesses.append(R[h]<R[j])
  S.add(z3.Implies(R[i]<R[j],z3.Or(witnesses)))
st=time.time();ans=S.check();print('result',ans,'seconds',time.time()-st,flush=True)
if ans==z3.sat:
 M=S.model();order=sorted(T,key=lambda f:M.eval(R[T.index(f)]).as_long())
 print('shelling',order,flush=True)
 Path('workspace/agent2_dunce_prism_shelling.json').write_text(json.dumps(order))
Path('workspace/agent2_dunce_prism_sat.py').write_text(Path(__file__).read_text())

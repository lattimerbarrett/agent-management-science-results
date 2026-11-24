import z3
from itertools import combinations
import sys,json
sys.path.insert(0,'workspace')
from agent1_shellability import shelling
from agent3_checker import certificate

def find_stuck(n,m,timeout=120000,normal=False):
 fs=[sum(1<<i for i in c) for c in combinations(range(n),m)]
 x={f:z3.Bool('f_'+str(f)) for f in fs}
 y={g:z3.Or([x[f] for f in fs if f&g==g]) for r in range(m) for c in combinations(range(n),r) for g in [sum(1<<i for i in c)]}
 s=z3.Solver();s.set(timeout=timeout)
 s.add(x[fs[0]],z3.Not(z3.And(list(x.values()))))
 for v in range(n):s.add(y[1<<v])
 dist={f:z3.Int('d_'+str(f)) for f in fs}
 for f in fs:
  s.add(dist[f]>=0,dist[f]<len(fs))
  if f==fs[0]:s.add(dist[f]==0)
  else:s.add(z3.Implies(x[f],z3.Or([z3.And(x[g],dist[g]<dist[f]) for g in fs if (f&g).bit_count()==m-1])))
  blocked=z3.Or([z3.And(x[g],*[z3.Not(y[f^(1<<v)]) for v in range(n) if (f>>v&1) and not(g>>v&1)]) for g in fs])
  s.add(z3.Or(x[f],blocked))
 if normal:
  for rank in range(1,m-1):
   for combo in combinations(range(n),rank):
    face=sum(1<<i for i in combo)
    sup=[f for f in fs if f&face==face]
    root={f:z3.Bool(f'root_{face}_{f}') for f in sup}
    d={f:z3.Int(f'ld_{face}_{f}') for f in sup}
    s.add(z3.PbEq([(root[f],1) for f in sup],1))
    for f in sup:
     # If the link is empty, the arbitrary root is permitted but has no connectivity obligation.
     s.add(z3.Implies(root[f],z3.Or(x[f],z3.Not(y[face]))))
     s.add(d[f]>=0,d[f]<len(sup))
     neigh=[z3.And(x[g],d[g]<d[f]) for g in sup if (f&g).bit_count()==m-1]
     s.add(z3.Implies(x[f],z3.Or(root[f],*neigh)))
 result=s.check();print(n,m,'normal='+str(normal),result,flush=True)
 if result==z3.sat:
  model=s.model();out=tuple(f for f in fs if z3.is_true(model[x[f]]))
  print('facets',out,flush=True)
  print('kdecomp',certificate(tuple(sorted(out)),m-1) is not None,flush=True)
  open(f'workspace/agent1_stuck_{n}_{m}.json','w').write(json.dumps(out))

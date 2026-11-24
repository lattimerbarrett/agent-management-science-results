import itertools,z3,json,time
from pathlib import Path
out=[]
for n in [14,17]:
 st=time.time();r=4;Es=[sum(1<<a for a in E) for E in itertools.combinations(range(n),r)];vs=[z3.Bool('e%d'%i) for i in range(len(Es))];s=z3.Solver();s.set(timeout=30000)
 for i,E in enumerate(Es):
  for j in range(i):
   if not E&Es[j]:s.add(z3.Or(z3.Not(vs[i]),z3.Not(vs[j])))
 for P in itertools.combinations(range(n),2):
  m=sum(1<<a for a in P)
  s.add(z3.Or([vs[i] for i,E in enumerate(Es) if E&m==m]))
 for P in itertools.combinations(range(n),r-1):
  m=sum(1<<a for a in P)
  s.add(z3.Or([vs[i] for i,E in enumerate(Es) if not E&m]))
 # anchor edge and private edge
 s.add(vs[0]);s.add(vs[Es.index(sum(1<<a for a in [3,4,5,6]))]);res=s.check();d={'n':n,'r':r,'result':str(res),'seconds':time.time()-st}
 if res==z3.sat:
  mod=s.model();d['edges']=[[a for a in range(n) if E>>a&1] for E,x in zip(Es,vs) if z3.is_true(mod[x])]
 out.append(d);print(d,flush=True)
Path('workspace/agent1_paircover_rank4.py').write_text(Path(__file__).read_text())
Path('workspace/agent1_paircover_rank4.json').write_text(json.dumps(out,indent=2))
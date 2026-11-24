import z3,itertools,json
from pathlib import Path
P=list(itertools.combinations(range(5),2))
graphs={'P3':[(0,1),(0,2)],'2K2':[(0,1),(2,3)],'P3+K2':[(0,1),(0,2),(3,4)],'P5':[(0,1),(1,2),(2,3),(3,4)],'C3+K2':[(0,1),(1,2),(0,2),(3,4)]}
R={}
for name,edges in graphs.items():
 E={tuple(sorted(e)) for e in edges};s=z3.Optimize();d={p:z3.Int('d%d%d'%p) for p in P};c={p:z3.Int('c%d%d'%p) for p in P}
 for p in P:
  s.add(d[p]>=-1,d[p]<=(0 if p in E else 5));s.add(c[p]==z3.Sum([z3.If(d[p]==j,1<<j,0) for j in range(6)]))
 for a,b in E:
  for i in range(5):
   if i in (a,b):continue
   x=tuple(sorted((i,a)));y=tuple(sorted((i,b)));s.add(z3.Implies(z3.And(d[x]>=0,d[y]>=0),d[x]+d[y]<=7))
 if name=='P3':s.add(c[(0,1)]+c[(0,2)]==1,c[(1,2)]==0)
 # For each any 3 nonedges of actual dimension5, transitivity prohibits a Q edge opposite.
 objective=z3.Sum(list(c.values()));s.maximize(objective);s.set(timeout=60000);status=s.check();print(name,status,flush=True)
 if status==z3.sat:
  m=s.model();vals={str(p):m.eval(c[p]).as_long() for p in P};v=m.eval(objective).as_long();R[name]={'pairmax':v,'pairs':vals};print(R[name],flush=True)
Path('workspace/agent4_fiveflat_pairmax.json').write_text(json.dumps(R,indent=2))
Path('workspace/agent4_fiveflat_pairmax.py').write_text(Path('scratchpad.py').read_text().split('
import itertools,z3,json,time
from pathlib import Path
out=[]
for r,n in [(4,10),(4,11),(4,12),(4,13)]: 
 st=time.time();Es=[tuple(E) for E in itertools.combinations(range(n),r)];masks=[sum(1<<a for a in E) for E in Es];vs=[z3.Bool('e%d'%i) for i in range(len(Es))];a=[z3.Real('a%d'%i) for i in range(n)];s=z3.Solver();s.set(timeout=30000)
 for i,E in enumerate(masks):
  for j in range(i):
   if not E&masks[j]:s.add(z3.Or(z3.Not(vs[i]),z3.Not(vs[j])))
 for P in itertools.combinations(range(n),2):
  m=sum(1<<a for a in P);s.add(z3.Or([vs[i] for i,E in enumerate(masks) if E&m==m]))
 for P in itertools.combinations(range(n),r-1):
  m=sum(1<<a for a in P);s.add(z3.Or([vs[i] for i,E in enumerate(masks) if not E&m]))
 s.add(z3.Sum(a)==-1)
 for x in a:s.add(x>=-1,x<=1)
 for E,x in zip(Es,vs):s.add(z3.Implies(x,z3.Sum([a[i] for i in E])>=0))
 for j in range(n-1):s.add(a[j]<=a[j+1])
 res=s.check();d={'n':n,'r':r,'result':str(res),'seconds':time.time()-st}
 if res==z3.sat:
  mod=s.model();d['edges']=[E for E,x in zip(Es,vs) if z3.is_true(mod[x])];d['weights']=[str(mod[x]) for x in a]
 out.append(d);print(d,flush=True)
Path('workspace/agent1_paircover_fpm_sorted.py').write_text(Path(__file__).read_text())
Path('workspace/agent1_paircover_fpm_sorted.json').write_text(json.dumps(out,indent=2))
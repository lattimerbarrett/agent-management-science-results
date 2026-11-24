import itertools as it,time,json
from pathlib import Path
import z3
start=time.time();results=[]
for n in [8,10]:
 w=3;t=6;U=set(range(n));cand=[]
 for a in range(1,w+1):
  for A0 in it.combinations(range(n),a):
   A=set(A0)
   for b in range(w-a+1):
    for D in it.combinations(U-A,b):cand.append((sum(1<<j for j in A),sum(1<<j for j in D)))
 vs=[z3.Bool(f'x_{n}_{j}') for j in range(len(cand))];sol=z3.Solver();sol.set(timeout=30000)
 nc=0
 for i,(A,D) in enumerate(cand):
  for j in range(i):
   B,E=cand[j]
   if not (A&E or B&D):sol.add(z3.Or(z3.Not(vs[i]),z3.Not(vs[j])));nc+=1
 for C in it.combinations(range(n),t-1):
  cm=sum(1<<j for j in C);sol.add(z3.Or(*[v for v,(A,D) in zip(vs,cand) if not A&cm]))
 cases=[]
 for a in range(1,w+1):
  # Any nonempty system has a term of some positive width a, then pad total width to w.
  A=(1<<a)-1;D=((1<<w)-1)^A
  jj=cand.index((A,D));sol.push();sol.add(vs[jj]);ts=time.time();ans=sol.check();witness=None
  if ans==z3.sat:
   model=sol.model();sel=[cand[j] for j,v in enumerate(vs) if z3.is_true(model.eval(v))]
   for i,(P,N) in enumerate(sel):
    for Q,M in sel[:i]:assert P&M or Q&N
   for C in it.combinations(range(n),t-1):
    cm=sum(1<<j for j in C);assert any(not P&cm for P,N in sel)
   witness=sel
  case={'a':a,'status':str(ans),'seconds':time.time()-ts,'witness':witness};cases.append(case);print(n,case,flush=True);sol.pop()
 results.append({'n':n,'width':w,'target_tau':t,'candidates':len(cand),'conflicts':nc,'cases':cases})
Path('workspace/agent2_udnf_width3_checks.py').write_text(Path('scratchpad.py').read_text());Path('workspace/agent2_udnf_width3_checks.json').write_text(json.dumps(results,indent=2));print('total_seconds',time.time()-start)

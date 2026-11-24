import itertools as it,time,json
from pathlib import Path
import z3
start=time.time();results=[]
for n in [10]:
 w=4;t=8;U=set(range(n));cand=[];byinput=[[] for x in range(1<<n)]
 for S in it.combinations(range(n),w):
  sm=sum(1<<j for j in S)
  for Amask in range(1,1<<w):
   A=sum(1<<S[j] for j in range(w) if Amask>>j&1);D=sm^A;cand.append((A,D))
 vs=[z3.Bool(f'x_{n}_{j}') for j in range(len(cand))];sol=z3.Solver();sol.set(timeout=60000)
 for j,(A,D) in enumerate(cand):
  free=((1<<n)-1)^(A|D);sub=free
  while True:
   byinput[A|sub].append(vs[j])
   if sub==0:break
   sub=(sub-1)&free
 for arr in byinput:
  if len(arr)>1:sol.add(z3.PbLe([(v,1) for v in arr],1))
 for C in it.combinations(range(n),t-1):
  cm=sum(1<<j for j in C);sol.add(z3.Or(*[v for v,(A,D) in zip(vs,cand) if not A&cm]))
 cases=[]
 print('built',n,len(cand),time.time()-start,flush=True)
 for a in range(1,w+1):
  A=(1<<a)-1;D=((1<<w)-1)^A;jj=cand.index((A,D));sol.push();sol.add(vs[jj]);ts=time.time();ans=sol.check();witness=None
  if ans==z3.sat:
   model=sol.model();sel=[cand[j] for j,v in enumerate(vs) if z3.is_true(model.eval(v))]
   for i,(P,N) in enumerate(sel):
    for Q,M in sel[:i]:assert P&M or Q&N
   for C in it.combinations(range(n),t-1):
    cm=sum(1<<j for j in C);assert any(not P&cm for P,N in sel)
   witness=sel
  case={'a':a,'status':str(ans),'seconds':time.time()-ts,'witness':witness};cases.append(case);print(n,case,flush=True);sol.pop()
 results.append({'n':n,'width':w,'target_tau':t,'candidates':len(cand),'cases':cases})
Path('workspace/agent2_udnf_width4_checks.py').write_text(Path('scratchpad.py').read_text());Path('workspace/agent2_udnf_width4_checks.json').write_text(json.dumps(results,indent=2));print('total_seconds',time.time()-start)

from itertools import combinations
from pathlib import Path
import z3,time,json,random
T=6;N=25;X=[set(range(4*i,4*i+4)) for i in range(T)];full=(1<<N)-1
E=[];cls=[]
for i in range(T):
 for p in combinations(set(range(N))-X[i],2):
  E.append(sum(1<<v for v in X[i]|set(p)));cls.append(i)
conflicts=[]
for i,e in enumerate(E):
 for j in range(i):
  if e&E[j]==0:conflicts.append((i,j))
print('candidates',len(E),'conflicts',len(conflicts),flush=True)
results=[]
for orbit,petal in [('ext_same',(4,24)),('ext_new',(4,24))]:
 st=time.time();s=z3.Solver();s.set(timeout=120000)
 x=[z3.Bool(orbit+str(i)) for i in range(len(E))]
 for i,j in conflicts:s.add(z3.Or(z3.Not(x[i]),z3.Not(x[j])))
 for j in range(T):s.add(z3.Or([x[i] for i in range(len(E)) if cls[i]==j]))
 anchor=sum(1<<v for v in X[0]|set(petal));s.add(x[E.index(anchor)])
 y=5 if orbit=='ext_same' else 12
 private_anchor=sum(1<<v for v in X[2]|{24,y});s.add(x[E.index(private_anchor)])
 cuts=set();iters=0;status='budget';best=0
 while time.time()-st<180:
  s.set(timeout=max(1,int((180-(time.time()-st))*1000)))
  ans=s.check()
  if ans!=z3.sat:status=str(ans);break
  model=s.model();chosen=[i for i in range(len(E)) if z3.is_true(model.eval(x[i],model_completion=True))]
  # Complete current family greedily; adding edges preserves every cover-cut.
  masks=[E[i] for i in chosen];present=set(chosen)
  for i,e in enumerate(E):
   if i not in present and all(e&f for f in masks):masks.append(e);chosen.append(i)
  best=max(best,len(masks));cs=z3.Solver();cs.set(timeout=10000);v=[z3.Bool(orbit+'v'+str(i)) for i in range(N)]
  cs.add(z3.PbLe([(p,1) for p in v],T-1))
  for e in masks:cs.add(z3.Or([v[p] for p in range(N) if e>>p&1]))
  nnew=0
  for rep in range(100):
   a=cs.check()
   if a==z3.unsat:
    if nnew==0:
     assert all(f&g for j,f in enumerate(masks) for g in masks[:j]);status='SAT_VALID_TAU6'
     Path('workspace/agent3_t6_rank6_d2_witness.json').write_text(json.dumps(dict(orbit=orbit,edges=masks,cores=[list(a) for a in X])))
    break
   if a!=z3.sat:status='cover_unknown';break
   m=cs.model();C=sum(1<<p for p in range(N) if z3.is_true(m.eval(v[p],model_completion=True)))
   assert all(e&C for e in masks)
   if C not in cuts:
    cut=[x[i] for i,e in enumerate(E) if not e&C];s.add(z3.Or(cut));cuts.add(C);nnew+=1
   cs.add(z3.Or([z3.Not(v[p]) for p in range(N) if C>>p&1]))
  iters+=1
  Path(f'workspace/agent3_t6_rank6_d2_private_{orbit}.smt2').write_text(s.to_smt2())
  if iters%10==0:print(orbit,'iterations',iters,'cuts',len(cuts),'family',len(masks),'elapsed',time.time()-st,flush=True)
  if status in ('SAT_VALID_TAU6','cover_unknown'):break
 row=dict(orbit=orbit,status=status,iterations=iters,cuts=len(cuts),largest_family=best,seconds=time.time()-st);results.append(row)
 print(row,flush=True)
 Path('workspace/agent3_t6_rank6_d2_private_branches.json').write_text(json.dumps(results,indent=2))

from itertools import combinations
from pathlib import Path
import z3,time,json

def cegar(n=9,q=3,seconds=180):
 M=[sum(1<<v for v in c) for c in combinations(range(n),q)];N=len(M);ix={m:i for i,m in enumerate(M)}
 P=[z3.Bool('p'+str(i)) for i in range(N)];R=[z3.Int('r'+str(i)) for i in range(N)]
 A=z3.Solver();O=z3.Solver();O.set(unsat_core=True,timeout=30000);A.set(timeout=30000)
 A.add(P[0],P[1],z3.PbLe([(p,1) for p in P],N-2))
 O.add(z3.Distinct([z3.If(P[i],R[i],N+i) for i in range(N)]))
 for i,r in enumerate(R):O.add(z3.If(P[i],z3.And(r>=0,r<N),r==N))
 for j,m in enumerate(M):
  blocks=[]
  for i,u in enumerate(M):
   if i==j:continue
   hs=[ix[(m^(1<<y))|(1<<x)] for x in range(n) if (u&~m)>>x&1 for y in range(n) if m>>y&1]
   O.add(z3.Implies(z3.And(P[j],R[i]<R[j]),z3.Or([z3.And(P[h],R[h]<R[j]) for h in hs])))
   blocks.append(z3.And(P[i],*[z3.Not(P[h]) for h in hs]))
   if (u&~m).bit_count()>=2:
    ni=[h for h,v in enumerate(M) if v&~(u|m)==0 and (v&~u).bit_count()==1]
    A.add(z3.Implies(z3.And(P[i],P[j]),z3.Or([P[h] for h in ni])))
  A.add(z3.Implies(z3.Not(P[j]),z3.Or(blocks)))
 neighbits=[sum(1<<j for j,v in enumerate(M) if (v&~u).bit_count()==1) for u in M]
 Ws=[sum(1<<i for i,u in enumerate(M) if u&~sum(1<<v for v in w)==0) for size in range(q+2,min(2*q,n)+1) for w in combinations(range(n),size)]
 def bits(b):
  while b:
   x=b&-b;b^=x;yield x.bit_length()-1
 st=time.time();iteration=0;graphcuts=0
 while time.time()-st<seconds:
  a=A.check()
  if a!=z3.sat:print('MASTER',a,'iter',iteration,'seconds',time.time()-st,flush=True);return
  model=A.model();lits=[p if z3.is_true(model.eval(p)) else z3.Not(p) for p in P]
  selected=sum(1<<i for i,p in enumerate(P) if z3.is_true(model.eval(p)))
  added=0
  for wb in Ws:
   rem=selected&wb
   if not rem:continue
   C=0;front=rem&-rem
   while front:
    C|=front
    grow=0
    for h in bits(front):grow|=neighbits[h]
    front=grow&rem&~C
   if C!=rem:
    boundary=0
    for h in bits(C):boundary|=neighbits[h]
    boundary&=wb&~C
    far=wb&~(C|boundary)
    A.add(z3.Implies(z3.And(z3.Or([P[h] for h in bits(C)]),z3.Or([P[h] for h in bits(far)])),z3.Or([P[h] for h in bits(boundary)])))
    added+=1
  if added:
   graphcuts+=added
   continue
  result=O.check(*lits)
  if result==z3.sat:
   rmodel=O.model();ordered=sorted([i for i,p in enumerate(P) if z3.is_true(model.eval(p))],key=lambda i:rmodel.eval(R[i]).as_long())
   out=[M[i] for i in ordered];print('COUNTEREXAMPLE',out,flush=True);Path('workspace/agent2_sat_counterexample.json').write_text(json.dumps({'n':n,'q':q,'generators':out}));return
  elif result==z3.unknown:
   print('ORACLE UNKNOWN iter',iteration,'seconds',time.time()-st,flush=True);return
  core=O.unsat_core();A.add(z3.Or([z3.Not(t) for t in core]));iteration+=1
  if iteration%100==0:print('cuts',iteration,'core',len(core),'selected',sum(z3.is_true(model.eval(p)) for p in P),'seconds',round(time.time()-st,1),flush=True)
 print('TIMEOUT',iteration,'seconds',time.time()-st,flush=True)

if __name__=='__main__':
 Path('workspace/agent2_cegar_sat.py').write_text(Path(__file__).read_text())
 cegar()

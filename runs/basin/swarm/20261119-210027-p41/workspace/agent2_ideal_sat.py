from itertools import combinations
from pathlib import Path
import z3,time,json

def sat(n,q,timeout=180000):
 masks=[sum(1<<v for v in c) for c in combinations(range(n),q)]; N=len(masks);index={v:i for i,v in enumerate(masks)}
 P=[z3.Bool('p'+str(i)) for i in range(N)];R=[z3.Int('r'+str(i)) for i in range(N)]
 S=z3.Solver();S.set(timeout=timeout)
 # Any counterexample has >=2 generators; vertex symmetry fixes its first two.
 S.add(P[0],R[0]==0,P[1],R[1]==1,z3.Distinct(R))
 for i in range(1,N):S.add(z3.If(P[i],z3.And(R[i]>=1,R[i]<N),R[i]==N+i))
 S.add(z3.PbLe([(p,1) for p in P],N-2))
 for j,m in enumerate(masks):
  witnesses=[]
  for i,u in enumerate(masks):
   if i==j:continue
   ix=[]
   for x in range(n):
    if (u&~m)>>x&1:
     for y in range(n):
      if m>>y&1:ix.append(index[(m^(1<<y))|(1<<x)])
   S.add(z3.Implies(z3.And(P[i],P[j],R[i]<R[j]),z3.Or([z3.And(P[h],R[h]<R[j]) for h in ix])))
   witnesses.append(z3.And(P[i],*[z3.Not(P[h]) for h in ix]))
  S.add(z3.Implies(z3.Not(P[j]),z3.Or(witnesses)))
 print('SAT built',n,q,'N',N,'constraints',len(S.assertions()),flush=True)
 t=time.time();ans=S.check();print('result',ans,'seconds',time.time()-t,flush=True)
 if ans==z3.sat:
  M=S.model();gens=[i for i in range(N) if z3.is_true(M.eval(P[i]))];gens.sort(key=lambda i:M.eval(R[i]).as_long())
  sol=[masks[i] for i in gens];print('SOLUTION',sol,flush=True);Path('workspace/agent2_sat_counterexample.json').write_text(json.dumps({'n':n,'q':q,'generators':sol}))
 elif ans==z3.unknown:print(S.reason_unknown(),flush=True)
 return ans

if __name__=='__main__':
 Path('workspace/agent2_ideal_sat.py').write_text(Path(__file__).read_text())
 assert sat(8,3,timeout=180000)==z3.unsat
 assert sat(8,4,timeout=180000)==z3.unsat

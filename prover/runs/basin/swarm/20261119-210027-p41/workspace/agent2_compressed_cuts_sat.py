from itertools import combinations
from pathlib import Path
import z3,time,json

def solve(n=10,q=3,timeout=180000):
 M=[sum(1<<v for v in c) for c in combinations(range(n),q)];N=len(M);ix={m:i for i,m in enumerate(M)}
 R=[z3.Int('r'+str(i)) for i in range(N)];S=z3.Solver();S.set(timeout=timeout)
 S.add(R[0]==0,R[1]==1,z3.Distinct([z3.If(r<N,r,N+i) for i,r in enumerate(R)]))
 for r in R:S.add(r>=0,r<=N)
 S.add(z3.Sum([z3.If(r<N,1,0) for r in R])<=N-2)
 T={}
 for j,m in enumerate(M):
  for x in range(n):
   if m>>x&1:continue
   t=z3.Int(f't{j}_{x}');T[j,x]=t
   neigh=[R[ix[(m^(1<<y))|(1<<x)]] for y in range(n) if m>>y&1]
   S.add(*[t<=r for r in neigh],z3.Or([t==r for r in neigh]))
 for j,m in enumerate(M):
  blocks=[]
  for i,u in enumerate(M):
   if i==j:continue
   ts=[T[j,x] for x in range(n) if (u&~m)>>x&1]
   if (u&~m).bit_count()>=2:
    # Necessary induced Johnson connectivity at the u endpoint.
    ni=[h for h,v in enumerate(M) if v&~(u|m)==0 and (v&~u).bit_count()==1]
    S.add(z3.Implies(z3.And(R[i]<N,R[j]<N),z3.Or([R[h]<N for h in ni])))
   S.add(z3.Implies(z3.And(R[j]<N,R[i]<R[j]),z3.Or([t<R[j] for t in ts])))
   blocks.append(z3.And(R[i]<N,*[t==N for t in ts]))
  S.add(z3.Implies(R[j]==N,z3.Or(blocks)))
 print('compressed SAT',n,q,N,'constraints',len(S.assertions()),flush=True)
 start=time.time();ans=S.check();print(ans,'seconds',time.time()-start,flush=True)
 if ans==z3.sat:
  model=S.model();ordered=sorted([i for i in range(N) if model.eval(R[i]).as_long()<N],key=lambda i:model.eval(R[i]).as_long())
  out=[M[i] for i in ordered];print('COUNTEREXAMPLE',out,flush=True);Path('workspace/agent2_sat_counterexample.json').write_text(json.dumps({'n':n,'q':q,'generators':out}))
 elif ans==z3.unknown:print(S.reason_unknown())
 return ans
if __name__=='__main__':
 pass
 solve(9,3)

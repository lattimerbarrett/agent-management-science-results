from itertools import combinations
import z3,time,json

def search(n,seconds=180,real=True):
 V=range(n);ff=list(combinations(V,4));tt=list(combinations(V,3));ee=list(combinations(V,2));N=len(ff)
 sets={f:set(f) for f in ff};S={t:z3.Bool('s'+str(t)) for t in tt};X={f:z3.Bool('x'+str(f)) for f in ff};E={e:z3.Bool('e'+str(e)) for e in ee}
 var=z3.Real if real else z3.Int;R={f:var('r'+str(f)) for f in ff};sol=z3.Solver();sol.set(timeout=seconds*1000)
 root=(0,1,2,3);second=(0,1,2,4)
 for f in ff:
  rr=list(combinations(f,3));sol.add(X[f]==z3.And([S[t] for t in rr]))
  sol.add(z3.Sum([z3.If(S[t],1,0) for t in rr])!=3)
  for a,b in combinations(rr,2):sol.add(z3.Implies(z3.And(S[a],S[b]),E[tuple(sorted(sets[f]-(set(a)&set(b))))]))
  if f==root:sol.add(R[f]==0)
  elif f==second:sol.add(R[f]==1)
  else:sol.add(R[f]>=2,R[f]<=N)
  sol.add(X[f]==(R[f]<N))
 sol.add(z3.Or([z3.Not(X[f]) for f in ff]))
 for t in tt:sol.add(S[t]==z3.Or([X[f] for f in ff if set(t)<=sets[f]]))
 for e in ee:sol.add(E[e]==z3.Or([X[f] for f in ff if set(e)<=sets[f]]))
 H={}
 for v in V:
  h=var('h'+str(v));H[v]=h;rs=[R[f] for f in ff if v in f]
  sol.add(h>=0,h<N,z3.Or([h==r for r in rs]));sol.add([h<=r for r in rs])
 for v in range(4,n-1):sol.add(H[v]<H[v+1])
 for f,g in combinations(ff,2):sol.add(z3.Or(z3.Not(X[f]),z3.Not(X[g]),R[f]!=R[g]))
 for f in ff:
  adj=[g for g in ff if len(sets[f]&sets[g])==3]
  if f!=root:sol.add(z3.Implies(X[f],z3.Or([R[g]<R[f] for g in adj])))
  for g in ff:
   h=sets[f]&sets[g]
   if not h or len(h)>2:continue
   cover=[e for e in adj if h<=sets[e]]
   sol.add(z3.Implies(z3.And(X[f],X[g],R[g]<R[f]),z3.Or([R[e]<R[f] for e in cover])))
 tm=time.time();ans=sol.check();print('directgeneral',n,'real',real,ans,'time',time.time()-tm,flush=True)
 if ans==z3.sat:
  m=sol.model();fac=sorted([f for f in ff if z3.is_true(m.eval(X[f]))],key=lambda f:float(m.eval(R[f]).as_fraction()))
  json.dump(fac,open('workspace/agent1_directgeneraltrap'+str(n)+'.json','w'));print(fac,flush=True)
 return ans
if __name__=='__main__':
 search(8,180,True)
 search(9,300,True)

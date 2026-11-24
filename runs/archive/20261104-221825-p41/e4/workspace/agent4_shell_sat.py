"""Exact bounded SAT encoding; no universal theorem is assumed."""
from itertools import combinations
from z3 import *

def instance(n,m,stuck=True,seed=True,timeout=100000):
 fs=[sum(1<<v for v in F) for F in combinations(range(n),m)]
 N=len(fs);s=Solver();s.set(timeout=timeout)
 t=[Int('t%d'%i) for i in range(N)]
 for i in range(N):s.add(t[i]>=0,t[i]<=N)
 if seed:
  s.add(t[0]==1)
  for i in range(1,N):s.add(t[i]!=1)
 else:s.add(Or([a==1 for a in t]))
 for i,j in combinations(range(N),2):s.add(Or(t[i]==0,t[j]==0,t[i]!=t[j]))
 for i,F in enumerate(fs):
  bits=[1<<v for v in range(n) if F>>v&1]
  ridges={v:[j for j,H in enumerate(fs) if j!=i and H&(F^v)==F^v] for v in bits}
  rp={v:Or([And(t[j]>0,t[j]<t[i]) for j in js]) for v,js in ridges.items()}
  for j,H in enumerate(fs):
   if i==j:continue
   s.add(Implies(And(t[i]>0,t[j]>0,t[j]<t[i]),Or([rp[v] for v in bits if not H&v])))
  if stuck:
   rf={v:Or([t[j]>0 for j in js]+[t[i]>0]) for v,js in ridges.items()}
   s.add(Or([And(t[j]>0,*[Not(rf[v]) for v in bits if not H&v]) for j,H in enumerate(fs)]))
 if stuck:s.add(Or([a==0 for a in t]))
 return s,fs,t

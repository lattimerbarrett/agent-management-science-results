from itertools import combinations
from z3 import *
import time,json
n=8
fs=[frozenset(f) for f in combinations(range(n),4)]
ts=[frozenset(t) for t in combinations(range(n),3)]
x=[Bool('f'+str(i)) for i in range(len(fs))]
r=[Int('r'+str(i)) for i in range(len(fs))]
y={t:Bool('t'+str(i)) for i,t in enumerate(ts)}
s=Solver();s.set(timeout=300000)
for i,f in enumerate(fs):
 s.add(r[i]>=0,r[i]<len(fs))
 s.add(Implies(Not(x[i]),r[i]==len(fs)-1))
 s.add(Implies(Not(x[i]),Sum([If(y[t],1,0) for t in ts if t<f])<=2))
for t in ts:s.add(y[t]==Or([x[i] for i,f in enumerate(fs) if t<f]))
for e in combinations(range(n),2):
 e=set(e);s.add(Or([x[i] for i,f in enumerate(fs) if e<f]))
s.add(Not(And(x)));s.add(x[0],r[0]==0,x[1],r[1]==1)
for i in range(2,len(fs)):s.add(Implies(x[i],r[i]>=2))
for v in range(5,n):
 for i,f in enumerate(fs):
  if v in f:
   s.add(Implies(x[i],Or([And(x[j],Or(r[j]<r[i],And(r[j]==r[i],j<i))) for j,g in enumerate(fs) if v-1 in g])))
for i,f in enumerate(fs):
 for j,g in enumerate(fs):
  if i==j:continue
  earlier=Or(r[j]<r[i],And(r[j]==r[i],j<i))
  common=f&g
  hs=[h for h,fh in enumerate(fs) if len(f&fh)==3 and common <= (f&fh)]
  s.add(Implies(And(x[i],x[j],earlier),Or([And(x[h],Or(r[h]<r[i],And(r[h]==r[i],h<i))) for h in hs])))
t=time.time();res=s.check();print(res,time.time()-t)
assert res==unsat

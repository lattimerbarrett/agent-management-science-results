from z3 import *
from itertools import combinations
from math import ceil,log2
import pickle,time
n=8;r=4
ff=[sum(1<<i for i in c) for c in combinations(range(n),r)]
M=len(ff);bits=ceil(log2(M+1))
proper=[sum(1<<i for i in c) for k in range(1,r) for c in combinations(range(n),k)]
t={f:BitVec('t'+str(f),bits) for f in ff+proper}
s=Solver();s.set(timeout=600000)
for f in ff+proper:s.add(ULE(t[f],M))
s.add(t[ff[0]]==0)
for f in ff[1:]:s.add(t[f]!=0)
for i,f in enumerate(ff):
 for g in ff[:i]:s.add(Or(t[f]==M,t[g]==M,t[f]!=t[g]))
L=Sum([If(t[f]!=M,1,0) for f in ff]);s.add(L<M)
for f in ff:s.add(Or(t[f]==M,BV2Int(t[f])<L))
for h in proper:
 inc=[t[f] for f in ff if f&h==h]
 s.add(*[ULE(t[h],a) for a in inc]);s.add(Or([t[h]==a for a in inc]))
for v in range(n):s.add(t[1<<v]!=M)
for v in range(4,n-1):s.add(ULT(t[1<<v],t[1<<(v+1)]))
for v in range(3):
 s.add(Sum([If(t[f]!=M,1,0) for f in ff if f>>v&1])>=Sum([If(t[f]!=M,1,0) for f in ff if f>>(v+1)&1]))
for f in ff:
 rr=[h for h in proper if h&f==h and h.bit_count()==3]
 low=[h for h in proper if h&f==h and h.bit_count()<3]
 if f!=ff[0]:s.add(Implies(t[f]!=M,Or([ULT(t[h],t[f]) for h in rr])))
 for h in low:
  s.add(Implies(And(t[f]!=M,ULT(t[h],t[f])),Or([ULT(t[g],t[f]) for g in rr if g&h==h])))
 bad=[And(t[h]!=M,*[t[g]==M for g in rr if g&h==h]) for h in low]
 s.add(Implies(t[f]==M,Or(bad)))
for vv in combinations(range(n),5):
 ss=sum(1<<i for i in vv)
 fs=[f for f in ff if f&ss==f]
 num=Sum([If(t[f]!=M,1,0) for f in fs])
 s.add(Or(num<=2,num==5))
for a,b in combinations(ff,2):
 if (a&b).bit_count()==3:
  ee=a^b
  s.add(Implies(And(t[a]!=M,t[b]!=M),t[ee]!=M))
print('starting',n,M,len(s.assertions()),flush=True)
start=time.time();res=s.check();print(res,time.time()-start,flush=True)
if res==sat:
 model=s.model();active=sorted([f for f in ff if model[t[f]].as_long()!=M],key=lambda f:model[t[f]].as_long())
 print(active,flush=True);pickle.dump((n,3,active),open('sat_stuck.pkl','wb'))

import math,itertools,time,json
from z3 import *
N=16384
orbits=[];od={};idx=[]
for x in range(N):
 c=[0]*4
 for i in range(6):c[((x>>i)&1)+2*((x>>(7+i))&1)]+=1
 c=tuple(c)+((x>>6)&1,(x>>13)&1)
 if c not in od:od[c]=len(orbits);orbits.append(c)
 idx.append(od[c])
w=[0]*len(orbits)
for j in idx:w[j]+=1
A=[1<<j for j in idx]
for i in range(14):
 for x in range(N):
  if x>>i&1:A[x]^=A[x^(1<<i)]
C=set(A[x] for x in range(N) if x.bit_count()>7)
b=[Bool(f'b{i}') for i in range(len(orbits))]
s=Solver();s.set(timeout=60000)
for c in C:
 bs=[b[j] for j in range(len(b)) if c>>j&1]
 if bs:
  q=bs[0]
  for z in bs[1:]:q=Xor(q,z)
  s.add(Not(q))
print('orbits',len(b),'constraints',len(C),flush=True)
for target in [310,322,326,330,334]:
 s.push();s.add(PbEq(list(zip(b,w)),target));t=time.time();ans=s.check();print(target,ans,time.time()-t,flush=True)
 if ans==sat:
  M=s.model();support=[i for i in range(N) if is_true(M[b[idx[i]]])];ss=set(support);truth=[int(i in ss) for i in range(N)]
  for j in range(14):
   for x in range(N):
    if x>>j&1:truth[x]^=truth[x^(1<<j)]
  anf=[x for x in range(N) if truth[x]]
  assert max(x.bit_count() for x in anf)<=7 and len(support)==target
  json.dump({'anf':anf,'orbits':[orbits[i] for i in range(len(b)) if is_true(M[b[i]])]},open(f'workspace/a1_symmetric_{target}.json','w'));print('ANF',len(anf),flush=True)
 s.pop()

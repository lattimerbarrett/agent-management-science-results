from z3 import *
import time,json
n=6;N=1<<n;b=[Bool('p%d'%i) for i in range(N)];a=b[:]
for j in range(n):
 for x in range(N):
  if x>>j&1:a[x]=Xor(a[x],a[x^(1<<j)])
s=SolverFor('QF_FD');s.set(timeout=30000)
for x in range(N):
 if x.bit_count()>=4:s.add(a[x] if x==15 else Not(a[x]))
s.add(PbEq([(x,1) for x in b],6))
t=time.time();r=s.check();print(r,time.time()-t);assert r==unsat
json.dump({'n':6,'degree':4,'top_decomposable':15,'weight':6,'answer':str(r)},open('workspace/agent4_decomposable_quartic_no6.json','w'))
open('workspace/agent4_decomposable_quartic_no6_checker.py','w').write(open('scratchpad.py').read())

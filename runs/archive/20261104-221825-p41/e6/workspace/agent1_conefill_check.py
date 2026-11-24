import sys,itertools
sys.path.insert(0,'workspace')
from agent2_decomp import *
count=0
for n in range(1,6):
 for q in range(1,n):
  fs0=[sum(1<<v for v in c) for c in itertools.combinations(range(n),q)]
  for flags in range(1,1<<len(fs0)):
   L=frozenset(f for i,f in enumerate(fs0) if flags>>i&1)
   fills=[sum(1<<v for v in c) for c in itertools.combinations(range(n),q+1) if all(sum(1<<v for v in z) in L for z in itertools.combinations(c,q))]
   for k in (0,1,2):
    if witness(L,k) is None:continue
    for bits in range(1<<len(fills)):
     T=frozenset(f|(1<<n) for f in L)|frozenset(f for i,f in enumerate(fills) if bits>>i&1)
     assert witness(T,k) is not None,(n,q,L,k,T)
     count+=1
print('cone plus fills cases passed',count)
open('workspace/agent1_conefill_check.py','w').write(open('scratchpad.py').read())
import sys,itertools,functools
sys.path.insert(0,'workspace')
from agent4_fastcert import fastcert
from agent3_check import all_faces,maximal,appendable
n=6;q=3;pool=[sum(1<<v for v in c) for c in itertools.combinations(range(n),q)]
L=[sum(1<<v for v in c) for c in [(0,2,3),(1,2,3),(0,1,4),(0,2,4),(1,2,4),(0,1,5),(0,3,5),(1,3,5)]]
base=sum(1<<i for i,f in enumerate(pool) if f in L);miss=[i for i,f in enumerate(pool) if f not in L]
def double(F):
 if fastcert(F,1) is None:return False
 H=all_faces(F)
 for v in range(n):
  fs=maximal(g for g in H if not g>>v&1)
  if not fs or any(f.bit_count()!=q for f in fs) or fastcert(fs,1) is None:return False
 return True
@functools.lru_cache(None)
def reach(mask,target):
 if mask==target:return True
 F=tuple(f for i,f in enumerate(pool) if mask>>i&1)
 for i,f in enumerate(pool):
  if target>>i&1 and not mask>>i&1 and appendable(F,f):
   if reach(mask|1<<i,target):return True
 return False
count=0
for mask in range(1<<len(miss)):
 target=base|sum(1<<i for j,i in enumerate(miss) if mask>>j&1)
 T=tuple(f for i,f in enumerate(pool) if target>>i&1)
 if not double(T):continue
 count+=1
 if not reach(base,target):print('COUNTER',L,T);raise SystemExit
print('PASS pairs',count)

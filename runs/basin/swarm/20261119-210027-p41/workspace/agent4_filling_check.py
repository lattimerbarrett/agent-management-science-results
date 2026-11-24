from itertools import combinations
from functools import lru_cache
n=6
@lru_cache(None)
def kd(fs,k):
 if len(fs)==1:return True
 if not fs:return False
 cand=set()
 for f in fs:
  vs=[v for v in range(n) if f>>v&1]
  for s in range(1,min(k+1,len(vs))+1):cand.update(sum(1<<v for v in c) for c in combinations(vs,s))
 for s in cand:
  dele=tuple(f for f in fs if f&s!=s)
  if not dele:continue
  yes=tuple(f for f in fs if f&s==s)
  if any(not any((f^(1<<v))&g==(f^(1<<v)) for g in dele) for f in yes for v in range(n) if s>>v&1):continue
  if kd(dele,k) and kd(tuple(sorted(f^s for f in yes)),k):return True
 return False
tri=tuple(sum(1<<v for v in c) for c in combinations(range(5),3))
tet=tuple(sum(1<<v for v in c) for c in combinations(range(5),4))
for k in (0,1,2):
 cases=0
 for m in range(1,1<<len(tri)):
  L=tuple(t for j,t in enumerate(tri) if m>>j&1)
  if not kd(L,k):continue
  allowed=tuple(f for f in tet if all(f^(1<<v) in L for v in range(5) if f>>v&1))
  for s in range(1<<len(allowed)):
   C=tuple(sorted(tuple(t|(1<<5) for t in L)+tuple(f for j,f in enumerate(allowed) if s>>j&1)))
   assert kd(C,k),(k,L,C)
   cases+=1
 print('k',k,'filling lemma instances verified',cases,flush=True)

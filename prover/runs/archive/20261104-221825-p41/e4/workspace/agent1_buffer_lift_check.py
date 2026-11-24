import sys
sys.path.insert(0,'workspace')
from agent3_checker import maximal,subsets,certificate,verify
from functools import lru_cache

def trunc(fs,r):
 return maximal(g for f in fs for s in range(min(r,f.bit_count())+1) for g in subsets(f,s))
complexes=set()
allmasks=tuple(range(16))
for bitset in range(1,1<<16):
 complexes.add(maximal(f for i,f in enumerate(allmasks) if bitset>>i&1))
print('complexes',len(complexes),flush=True)
count=0
for fs in complexes:
 for p in range(4):
  U=((1<<p)-1)<<4
  for r in range(1,5+p):
   q=max(0,r-p)
   low=trunc(fs,q)
   high=trunc(tuple(f|U for f in fs),r)
   if max(f.bit_count() for f in low)!=q:continue
   for k in (0,1):
    lc=certificate(low,k)
    if lc is None:continue
    hc=certificate(high,k)
    assert hc is not None,(fs,p,r,k,low,high)
    verify(high,k,hc)
    count+=1
print('Buffer lifting classifications independently verified',count,flush=True)

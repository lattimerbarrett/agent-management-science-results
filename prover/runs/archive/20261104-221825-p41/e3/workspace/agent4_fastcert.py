import json,itertools,time,functools
from collections import Counter
@functools.lru_cache(None)
def fastcert(fs,k):
 if len(fs)==1:return ('s',fs[0])
 if not fs:return None
 r=fs[0].bit_count()
 if any(f.bit_count()!=r for f in fs):return None
 ridges=Counter(f^(1<<v) for f in fs for v in range(f.bit_length())if f>>v&1)
 candidates=set()
 for f in fs:
  vs=[v for v in range(f.bit_length())if f>>v&1]
  for z in range(1,min(k+1,r)+1):
   for c in itertools.combinations(vs,z):candidates.add(sum(1<<v for v in c))
 good=[]
 for s in candidates:
  contain=[f for f in fs if f&s==s]
  if not contain or len(contain)==len(fs):continue
  if any(ridges[f^(1<<v)]==1 for f in contain for v in range(s.bit_length())if s>>v&1):continue
  link=tuple(sorted(f^s for f in contain))
  good.append((len(contain),s,link))
 # prefer largest removed star to reduce search
 good.sort(reverse=True)
 for _,s,link in good:
  lc=fastcert(link,k)
  if lc is None:continue
  ds=tuple(f for f in fs if f&s!=s)
  dc=fastcert(ds,k)
  if dc is not None:return ('d',s,dc,lc)
 return None
if __name__=='__main__':
 import sys
 sys.path.insert(0,'workspace')
 from agent3_check import k_certificate
 checked=0
 for n,r in [(5,3),(6,4)]:
  allfs=[sum(1<<v for v in q)for q in itertools.combinations(range(n),r)]
  for mask in range(1,1<<len(allfs)):
   fs=tuple(sorted(f for i,f in enumerate(allfs)if mask>>i&1))
   for k in [0,1]:
    assert bool(fastcert(fs,k))==bool(k_certificate(fs,k)),(fs,k)
    checked+=1
  print('verified',n,r,checked,flush=True)
 with open('workspace/agent4_fastcert.py','w')as out:out.write(open(__file__).read())

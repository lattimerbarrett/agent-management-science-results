import itertools,functools
from collections import Counter
@functools.lru_cache(maxsize=300000)
def kd(fs,k):
 if len(fs)<=1:return True
 q=fs[0].bit_count()
 counts=Counter(f^(1<<v) for f in fs for v in range(f.bit_length()) if f>>v&1)
 verts=0
 for f in fs:verts|=f
 vv=[i for i in range(verts.bit_length()) if verts>>i&1]
 for size in range(1,min(q,k+1)+1):
  for cc in itertools.combinations(vv,size):
   s=sum(1<<v for v in cc);contained=[f for f in fs if f&s==s]
   if not contained:continue
   if any(counts[f^(1<<v)]<2 for f in contained for v in cc):continue
   rest=tuple(f for f in fs if f&s!=s)
   link=tuple(sorted(f^s for f in contained))
   if kd(link,k) and kd(rest,k):return True
 return False

from itertools import combinations
from functools import lru_cache
from sage.all import simplicial_complexes
import random

def bits(x):
 while x:
  y=x&-x;yield y;x-=y

def maximal(fs):
 fs=set(fs)
 return tuple(sorted(f for f in fs if not any(f!=g and f&g==f for g in fs)))

@lru_cache(None)
def kd(fs,k):
 if len(fs)==1:return True
 ranks={f.bit_count() for f in fs}
 if len(ranks)!=1:return False
 q=next(iter(ranks));faces=set()
 for f in fs:
  vs=list(bits(f))
  for s in range(1,min(k+1,q)+1):
   for t in combinations(vs,s):faces.add(sum(t))
 for s in sorted(faces,key=lambda x:(x.bit_count(),x)):
  de=[];li=[]
  for f in fs:
   if f&s==s:
    li.append(f^s);de.extend(f^v for v in bits(s))
   else:de.append(f)
  de=maximal(de)
  if any(f.bit_count()!=q for f in de):continue
  if kd(de,k) and kd(maximal(li),k):return True
 return False

random.seed(2026)
for example in [simplicial_complexes.ZieglerBall(),simplicial_complexes.RudinBall()]:
 full=tuple(sorted(sum(1<<int(v) for v in F) for F in example.facets()))
 sk=tuple(sorted({f^v for f in full for v in bits(f)}))
 print(str(example),'full skeleton vdec?',kd(sk,0),flush=True)
 facets=[sum(1<<int(v) for v in F) for F in example.facets()]
 n=max(f.bit_length() for f in facets);q=4;a=1<<n
 for trial in range(200):
  fs=(random.choice(facets),)
  while True:
   opts=[f for f in facets if f not in fs and all(g.bit_count()==q-1 for g in maximal(f&g for g in fs))]
   if not opts:break
   fs=tuple(sorted(fs+(random.choice(opts),)))
   if not kd(fs,0):
    print('non-vdec shellable',len(fs),fs,flush=True)
    cone=tuple(sorted(set(fs)|{a+(f^v) for f in fs for v in bits(f)}))
    print('apex closure vdec?',kd(cone,0), '1-dec?',kd(fs,1),flush=True)
    break
  else:continue
  if not kd(fs,0):break
 print('done',str(example),flush=True)

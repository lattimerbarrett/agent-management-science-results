from functools import lru_cache
from itertools import combinations
import sys, random
sys.path.insert(0,'workspace')
from agent4_checker import dec

def subs(s):
 x=s
 while True:
  yield x
  if not x:return
  x=(x-1)&s

def rankfaces(n,D):
 return [sum(1<<v for v in c) for c in combinations(range(n),D)]

def skeleton(F,D):
 return tuple(sorted({s for f in F for s in subs(f) if s.bit_count()==D}))

def faces(F):return {s for f in F for s in subs(f)}

def attachable(old,F):
 R=sum(1<<v for v in range(F.bit_length()) if F>>v&1 and F^(1<<v) in old)
 return R not in old

@lru_cache(None)
def shelling(F):
 if len(F)==1:return F
 for f in F:
  rest=tuple(g for g in F if g!=f)
  if attachable(faces(rest),f):
   sh=shelling(rest)
   if sh:return sh+(f,)
 return None

def completion(F,V,A):
 '''Return added facet sequence; assumes shellable pure rank D and |A|=max(0,D-3).'''
 F=tuple(sorted(F));D=F[0].bit_count();assert shelling(F)
 assert len(A)==max(0,D-3)
 old=faces(F);add=[]
 def append(f):
  nonlocal old
  assert f not in old
  assert attachable(old,f)
  old.update(subs(f));add.append(f)
 if D<=3:
  # Connected graph for D=2; connected one-skeleton for D=3.
  while True:
   missing=[sum(1<<v for v in c) for c in combinations(V,D) if sum(1<<v for v in c) not in old]
   if not missing:break
   good=next((f for f in missing if attachable(old,f)),None)
   assert good is not None
   append(good)
  return add
 a=A[0];abit=1<<a;L=skeleton(F,D-1)
 for h in shelling(L):append(abit|h)
 lower=completion(L,V,A[1:])
 for h in lower:append(abit|h)
 W=tuple(V)+tuple(A[1:])
 for c in combinations(W,D):
  f=sum(1<<v for v in c)
  if f not in old:append(f)
 assert old==faces(tuple(sum(1<<v for v in c) for c in combinations(tuple(V)+tuple(A),D)))
 return add

def run():
 random.seed(42)
 count=0;stages=0
 for n,D in [(5,3),(6,4),(7,5)]:
  allF=rankfaces(n,D)
  for trial in range(25):
   F=tuple(sorted(random.sample(allF,random.randint(1,len(allF)))))
   if not shelling(F):continue
   V=tuple(v for v in range(n) if any(f>>v&1 for f in F));A=tuple(range(n,n+max(0,D-3)))
   added=completion(F,V,A)
   cur=list(F)
   for f in added:
    cur.append(f)
    assert dec(tuple(sorted(cur)),D-1)
    stages+=1
   assert len(cur)==len(list(combinations(V+A,D)))
   count+=1
 print('Verified shellable upper-bound algorithm:',count,'input complexes;',stages,'independently k-decomposability-checked additions')
if __name__=='__main__':run()

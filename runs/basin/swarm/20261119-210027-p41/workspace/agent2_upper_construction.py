from itertools import combinations
from functools import lru_cache
from pathlib import Path
import random

def subs(f,s):
 return tuple(sum(c) for c in combinations([1<<v for v in range(f.bit_length()) if f>>v&1],s))

@lru_cache(None)
def witness(fs,k):
 if len(fs)==1:return (0,(),())
 if not fs:return None
 vertices=0
 for f in fs:vertices|=f
 size=fs[0].bit_count()
 for c in range(1,min(k+1,size)+1):
  for s in subs(vertices,c):
   D=tuple(f for f in fs if f&s!=s)
   if not D or len(D)==len(fs):continue
   L=tuple(sorted(f^s for f in fs if f&s==s))
   exposed=[f^v for f in fs if f&s==s for v in subs(s,1)]
   if any(not any(g&h==h for g in D) for h in exposed):continue
   if witness(D,k) is not None and witness(L,k) is not None:return s,D,L
 return None

def cone_ridge_order(fs,a,k):
 d=fs[0].bit_count()-1
 if d<0:return []
 s,D,L=witness(fs,k)
 if s==0:return [a|f for f in subs(fs[0],d)]
 return cone_ridge_order(D,a,k)+[s|f for f in cone_ridge_order(L,a,k)]

def vertices(fs):
 ans=0
 for f in fs:ans|=f
 return ans

def complete(fs,k,extras):
 # facets fs in dimension >=2, vertex set exactly its union
 fs=tuple(sorted(fs));size=fs[0].bit_count();d=size-1;V=vertices(fs)
 assert witness(fs,k) is not None
 if d==2:
  assert not extras
  state=set(fs);edge=set(e for f in fs for e in subs(f,2));order=[]
  # Connected graph, so length-two paths can complete its graph.
  while len(edge)<V.bit_count()*(V.bit_count()-1)//2:
   found=False
   for f in subs(V,3):
    E=subs(f,2)
    if sum(e in edge for e in E)==2:
     assert f not in state
     state.add(f);edge.update(E);order.append(f);found=True;break
   assert found,'graph unexpectedly disconnected'
  order += [f for f in subs(V,3) if f not in state]
  return order
 assert len(extras)==d-2
 a=extras[0]
 order=cone_ridge_order(fs,a,k)
 shadow=tuple(sorted({r for f in fs for r in subs(f,d)}))
 order += [a|r for r in complete(shadow,k,extras[1:])]
 W=V
 for b in extras:W|=b
 state=set(fs)|set(order)
 order += [f for f in subs(W,size) if not f&a and f not in state]
 return order

def test():
 rng=random.Random(39)
 # Produce a shellable complex by taking prefixes of known VD simplex-skeleton order.
 for d,n,k in [(3,6,1),(3,7,1),(4,6,1)]:
  allfacets=list(subs((1<<n)-1,d+1));count=0
  for trial in range(12):
   # Random dense facet sets; exact witness oracle determines admissibility.
   fs=tuple(sorted(rng.sample(allfacets,rng.randint(1,len(allfacets)))))
   if witness(fs,k) is None:continue
   V=vertices(fs);extras=[1<<(n+i) for i in range(d-2)]
   order=complete(fs,k,extras)
   state=set(fs)
   for f in order:
    assert f not in state
    state.add(f)
    assert witness(tuple(sorted(state)),k) is not None,(d,n,k,trial,f)
   W=V
   for b in extras:W|=b
   assert state==set(subs(W,d+1))
   count+=1
  print('Upper construction checked d,n,k =',d,n,k,'inputs',count,flush=True)
 print(witness.cache_info(),flush=True)

if __name__=='__main__':
 test()
 Path('workspace/agent2_upper_construction.py').write_text(Path(__file__).read_text())

"""Explicit lower-bound family and exact recursive-decomposition checks.
Only Python standard-library imports.  Default run verifies d=3, 7960 facets.
"""
from itertools import combinations, product
from functools import lru_cache
from collections import Counter

TRIANGLES = [(0,1,2),(0,2,3),(1,2,4),(2,3,4),(0,1,5),
 (1,4,5),(0,3,5),(3,5,6),(5,6,7),(3,4,6),(4,5,7),
 (3,4,7),(1,4,6),(1,6,7),(1,3,7),(0,1,7),(0,4,7),
 (0,4,6),(0,2,6),(2,5,6),(0,2,7)]
BARRIER = set(TRIANGLES) | {(1,2,7)}

def bits(x):
 while x:
  b=x&-x;yield b;x-=b

def masks(U,r):
 return {sum(c) for c in combinations(tuple(bits(U)),r)}

@lru_cache(None)
def uniform_certificate(U,r):
 if r==0:return ('simplex',0)
 assert U.bit_count()>=r
 if U.bit_count()==r:return ('simplex',U)
 v=U&-U
 return ('shed',v,uniform_certificate(U^v,r),uniform_certificate(U^v,r-1))

def base_checks():
 E=set();V=set();restrictions=[]
 for i,t in enumerate(TRIANGLES):
  R=tuple(v for v in t if tuple(w for w in t if w!=v) in E)
  if i:
   assert len(R) in (1,2)
   old_edges=[e for e in combinations(t,2) if e in E]
   assert all(any(v in e for e in old_edges) for v in t if v in V)
  restrictions.append(R)
  E.update(combinations(t,2));V.update(t)
 assert V==set(range(8)) and len(E)==28 and len(TRIANGLES)==21
 assert 8-28+21==1
 assert (0,1,3) not in BARRIER and len(BARRIER)==22
 h=Counter(sum(t in BARRIER for t in combinations(f,3))
           for f in combinations(range(8),4))
 assert h=={0:9,1:14,2:46,4:1}
 return restrictions

def construct(d):
 assert d>=3
 q=m=d+1;Rlist=base_checks()
 def cluster(v):return sum(1<<(m*v+j) for j in range(m))
 initial=sum(cluster(v) for v in TRIANGLES[0])
 facets=masks(initial,q);cert=uniform_certificate(initial,q)
 for F,R in zip(TRIANGLES[1:],Rlist[1:]):
  s=len(R)
  for indices in sorted(product(range(m),repeat=s),reverse=True):
   sigma=sum(1<<(m*v+i) for v,i in zip(R,indices))
   U=sum(cluster(v) for v in F if v not in R)
   U |= sum(1<<(m*v+j) for v,i in zip(R,indices)
            for j in range(i+1,m))
   link=masks(U,q-s)
   new={sigma|f for f in link}
   assert not (new & facets)
   facets |= new
   cert=('shed',sigma,cert,uniform_certificate(U,q-s))
 expected=set()
 for F in TRIANGLES:expected |= masks(sum(cluster(v) for v in F),q)
 assert facets==expected
 return tuple(sorted(facets)),cert

def verify_uniform(facets,k,cert):
 # Check the recursive definition, without assuming the construction lemmas.
 todo=[(tuple(sorted(set(facets))),cert)];seen=set();nodes=visits=0
 while todo:
  fs,c=todo.pop();key=(fs,id(c))
  if key in seen:continue
  seen.add(key);nodes+=1;visits+=len(fs)
  assert fs
  q=fs[0].bit_count();assert all(f.bit_count()==q for f in fs)
  if c[0]=='simplex':
   assert fs==(c[1],);continue
  assert c[0]=='shed'
  sigma=c[1];assert sigma and sigma.bit_count()<=k+1
  de=tuple(f for f in fs if f&sigma!=sigma)
  removed=[f for f in fs if f&sigma==sigma]
  assert de and removed
  # Every potential lower-dimensional deletion facet is covered by a
  # remaining q-facet iff each F-v, v in sigma, occurs among its ridges.
  ridges={f^v for f in de for v in bits(f)}
  assert all(f^v in ridges for f in removed for v in bits(sigma))
  li=tuple(sorted({f^sigma for f in removed}))
  todo.extend(((de,c[2]),(li,c[3])))
 return nodes,visits

def verify_barrier(facets,d):
 m=d+1;n=8*m
 def in_barrier(t):
  p=tuple(sorted({v//m for v in t}))
  return len(p)<3 or p in BARRIER
 assert not in_barrier((0,m,3*m))
 S={t for t in combinations(range(n),3) if in_barrier(t)}
 assert all(sum(t in S for t in combinations(f,3))!=3
            for f in combinations(range(n),4))
 E=set();T=set()
 for f in facets:
  vv=[b.bit_length()-1 for b in bits(f)]
  E.update(combinations(vv,2));T.update(combinations(vv,3))
 assert len(E)==n*(n-1)//2 and T<=S
 return len(E),len(T),len(S)

if __name__=='__main__':
 d=3
 facets,cert=construct(d)
 nodes,visits=verify_uniform(facets,1,cert)
 e,t,s=verify_barrier(facets,d)
 print('VERIFIED',dict(d=d,vertices=8*(d+1),facets=len(facets),
       certificate_nodes=nodes,facet_visits=visits,edges=e,
       triangles=t,barrier_triangles=s))

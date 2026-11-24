from itertools import combinations,product
from functools import lru_cache
from math import comb

T0=[(0,1,2),(0,2,3),(1,2,4),(2,3,4),(0,1,5),(1,4,5),(0,3,5),(3,5,6),(5,6,7),(3,4,6),(4,5,7),(3,4,7),(1,4,6),(1,6,7),(1,3,7),(0,1,7),(0,4,7),(0,4,6),(0,2,6),(2,5,6),(0,2,7)]
S=set(T0)|{(1,2,7)}

def bits(f):
 out=[]
 while f:
  b=f&-f;out.append(b);f^=b
 return out

def base_certificate():
 old={0};cert=None;restrictions=[]
 for tri in T0:
  f=sum(1<<v for v in tri)
  if cert is None:cert=('simplex',f);R=()
  else:
   rr=[v for v in tri if f^(1<<v) in old]
   r=sum(1<<v for v in rr)
   assert len(rr) in (1,2)
   for j in range(4):
    for cc in combinations(tri,j):
     g=sum(1<<v for v in cc)
     assert (g not in old)==(g&r==r)
   cert=('shed',r,cert,('simplex',f^r));R=tuple(rr)
  restrictions.append(R)
  for j in range(4):
   old.update(sum(1<<v for v in cc) for cc in combinations(tri,j))
 assert sum(g.bit_count()==1 for g in old)==8
 assert sum(g.bit_count()==2 for g in old)==28
 assert 8-28+len(T0)==1
 assert S!=set(combinations(range(8),3))
 assert all(sum(t in S for t in combinations(Q,3))!=3 for Q in combinations(range(8),4))
 return tuple(sum(1<<v for v in t) for t in T0),cert,restrictions

@lru_cache(None)
def uniform(U,r):
 if r==0:return ('simplex',0)
 assert U.bit_count()>=r
 if U.bit_count()==r:return ('simplex',U)
 v=U&-U
 return ('shed',v,uniform(U^v,r),uniform(U^v,r-1))

def construct(q,m=None):
 if m is None:m=q
 assert q>=4 and (m>=q or (q,m)==(4,2))
 _,_,restrictions=base_certificate()
 out=[];cert=None;phases=0
 for tri,R in zip(T0,restrictions):
  if cert is None:
   U=sum(1<<(v*m+j) for v in tri for j in range(m))
   out.extend(sum(cc) for cc in combinations(bits(U),q));cert=uniform(U,q)
   continue
  s=len(R);r=q-s
  for inds in product(range(m-1,-1,-1),repeat=s):
   sig=sum(1<<(v*m+j) for v,j in zip(R,inds))
   U=sum(1<<(v*m+j) for v in tri if v not in R for j in range(m))
   U|=sum(1<<(v*m+j) for v,i in zip(R,inds) for j in range(i+1,m))
   out.extend(sig|sum(cc) for cc in combinations(bits(U),r))
   cert=('shed',sig,cert,uniform(U,r));phases+=1
 expected=21*comb(3*m,q)-35*comb(2*m,q)+15*comb(m,q)
 assert len(out)==len(set(out))==expected
 return tuple(out),cert,phases

def verify_barrier(facets,q,m):
 N=8*m
 oldT={sum(1<<v for v in t) for t in T0}
 actual={sum(cc) for f in facets for cc in combinations(bits(f),3)}
 def projected(t):return tuple(sorted(set(v//m for v in t)))
 barrier={sum(1<<v for v in t) for t in combinations(range(N),3) if len(projected(t))<=2 or projected(t) in S}
 expected={sum(1<<v for v in t) for t in combinations(range(N),3) if len(projected(t))<=2 or projected(t) in set(T0)}
 assert actual==expected and actual<=barrier
 assert len(barrier)<comb(N,3)
 E={sum(cc) for f in facets for cc in combinations(bits(f),2)}
 assert len(E)==comb(N,2)
 assert all(sum((Q^(1<<v)) in barrier for v in range(N) if Q>>v&1)!=3 for Q in (sum(1<<v for v in a) for a in combinations(range(N),4)))
 return len(E),len(actual),len(barrier)

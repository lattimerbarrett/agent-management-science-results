"""Constructive relative vertex-decomposition for targets with >=rank join factors."""
from functools import lru_cache
from agent3_checker import subsets,deletion_link,verify
from agent2_vertex_completion import certified_completion

@lru_cache(None)
def factor_data(T):
 r=T[0].bit_count();U=0
 for F in T:U|=F
 negatives=[]
 for size in range(2,r+1):
  for s in subsets(U,size):
   if not any(s&F==s for F in T) and not any(t&s==t for t in negatives):negatives.append(s)
 bits=list(subsets(U,1));parent={v:v for v in bits}
 def root(v):
  while parent[v]!=v:
   parent[v]=parent[parent[v]];v=parent[v]
  return v
 used=0
 for s in negatives:
  b=list(subsets(s,1));used|=s
  for v in b[1:]:parent[root(v)]=root(b[0])
 count=len({root(v) for v in bits})
 return U,used,count,tuple(negatives)

def factor_completion(target,W):
 T=tuple(sorted(target));r=W.bit_count()
 assert W in T and all(F.bit_count()==r for F in T)
 if len(T)==1:return ()
 U,used,count,negatives=factor_data(T)
 assert count>=r,(T,W,count,r)
 outside=used&~W
 if not outside:
  assert not negatives and set(T)==set(subsets(U,r))
  return certified_completion((W,),('simplex',W),U)
 u=outside&-outside
 D,L=deletion_link(T,u)
 assert all(F.bit_count()==r for F in D)
 out=list(factor_completion(D,W))
 dc=out[-1][1] if out else ('simplex',W)
 S=L[0]
 out.append((u|S,('shed',u,dc,('simplex',S))))
 for g,gc in factor_completion(L,S):out.append((u|g,('shed',u,dc,gc)))
 cur={W}
 for F,c in out:
  assert F in T and F not in cur
  cur.add(F);verify(tuple(sorted(cur)),0,c)
 assert cur==set(T)
 return tuple(out)

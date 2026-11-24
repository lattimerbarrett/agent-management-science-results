import sys,json,time
from functools import lru_cache
from pathlib import Path
sys.path.insert(0,'workspace')
from agent4_minroots import roots,certificate,deletion_link,subsets
@lru_cache(None)
def leafdomains(fs,T):
 if len(fs)==1:return frozenset([T])
 ans=set()
 for s in roots(fs,1):
  D,L=deletion_link(fs,s);DT,LT=deletion_link(T,s)
  ans.update(leafdomains(D,DT));ans.update(leafdomains(L,LT))
 return frozenset(ans)
@lru_cache(None)
def matroid(T):
 S=set(T)
 for A in T:
  for B in T:
   for a in subsets(A&~B,1):
    if not any((A^a^b) in S for b in subsets(B&~A,1)):return False
 return True
@lru_cache(None)
def buffer(T):
 r=T[0].bit_count();U=0
 for f in T:U|=f
 nf=[]
 for q in range(2,r+1):
  for s in subsets(U,q):
   if not any(s&f==s for f in T) and not any(t&s==t for t in nf):nf.append(s)
 constrained=0
 for s in nf:constrained|=s
 p=(U&~constrained).bit_count()
 return r,p,tuple(nf)

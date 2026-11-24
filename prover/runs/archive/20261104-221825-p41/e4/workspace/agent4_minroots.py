import sys,json,itertools,random,time
from functools import lru_cache
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_checker import certificate,deletion_link,verify,subsets
@lru_cache(None)
def roots(fs,k):
 if len(fs)==1:return ()
 r=fs[0].bit_count()
 faces={s for F in fs for q in range(1,min(k+1,r)+1) for s in subsets(F,q)}
 ans=[];size=1
 for q in range(1,min(k+1,r)+1):
  for s in sorted(x for x in faces if x.bit_count()==q):
   D,L=deletion_link(fs,s)
   if any(x.bit_count()!=r for x in D):continue
   if certificate(D,k) and certificate(L,k):ans.append(s)
  if ans:return tuple(ans)
 raise AssertionError(fs)
def random_cert(fs,k):
 if len(fs)==1:return ('simplex',fs[0])
 s=random.choice(roots(fs,k));D,L=deletion_link(fs,s)
 return ('shed',s,random_cert(D,k),random_cert(L,k))
def target_check(T,c,k,path=()):
 if len({f.bit_count() for f in T})!=1:return ('impure',path,T)
 if c[0]=='simplex':
  if certificate(T,k) is None:return ('badleaf',path,T)
  return None
 s=c[1];D,L=deletion_link(T,s)
 if not D or any(f.bit_count()!=T[0].bit_count() for f in D):return ('baddelete',path+(s,),D)
 return target_check(D,c[2],k,path+(s,)) or target_check(L,c[3],k,path+(-s,))

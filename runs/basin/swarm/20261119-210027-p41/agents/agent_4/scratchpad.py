import pickle,time
from functools import lru_cache
L=pickle.load(open('workspace/agent4_nonvd_shellable2_n6.pkl','rb'));n=12
orig=tuple(sum(1<<v for v in f+tuple(x+6 for x in g)) for f in L for g in L)
sk=tuple(sorted(set(f^(1<<v) for f in orig for v in range(n) if f>>v&1)))
@lru_cache(None)
def vd(fs):
 if len(fs)==1:return True
 if fs[0].bit_count()<=1:return True
 co={}
 for f in fs:
  for v in range(n):
   if f>>v&1:co[f^(1<<v)]=co.get(f^(1<<v),0)+1
 for v in range(n):
  yes=tuple(f for f in fs if f>>v&1);no=tuple(f for f in fs if not f>>v&1)
  if not no or not yes:continue
  if any(co[f^(1<<v)]==1 for f in yes):continue
  if vd(no) and vd(tuple(sorted(f^(1<<v) for f in yes))):return True
 return False
t=time.time();print('GammaGamma skeleton',len(sk),'VD',vd(sk),vd.cache_info(),time.time()-t)

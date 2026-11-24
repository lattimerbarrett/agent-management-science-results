import pickle,itertools,random,time
from functools import lru_cache
n=9;L=pickle.load(open('workspace/agent4_nonvd_shellable2.pkl','rb'));start=tuple(sorted((1<<8)|sum(1<<v for v in f) for f in L));allfs=tuple(sum(1<<v for v in f) for f in itertools.combinations(range(n),4))
@lru_cache(None)
def kd(fs,k):
 if len(fs)==1:return True
 size=fs[0].bit_count()
 if size<=1:return True
 if size==2:
  seen=fs[0]
  while True:
   new=seen
   for f in fs:
    if f&seen:new|=f
   if new==seen:return all(f&seen for f in fs)
   seen=new
 counts={}; inds={}
 for f in fs:
  vv=[v for v in range(n) if f>>v&1];inds[f]=vv
  for v in vv:counts[f^(1<<v)]=counts.get(f^(1<<v),0)+1
 bad={f:sum(1<<v for v in inds[f] if counts[f^(1<<v)]==1) for f in fs}
 cand=set()
 for f in fs:
  for z in range(1,min(k+1,size)+1):cand.update(sum(1<<v for v in c) for c in itertools.combinations(inds[f],z))
 for s in sorted(cand,key=int.bit_count):
  yes=tuple(f for f in fs if f&s==s)
  if any(bad[f]&s for f in yes):continue
  no=tuple(f for f in fs if f&s!=s)
  if not no:continue
  if kd(tuple(sorted(f^s for f in yes)),k) and kd(no,k):return True
 return False

def shelladd(fs,f):
 faces=set(g&f for g in fs)
 maxi=[h for h in faces if not any(h!=j and h&j==h for j in faces)]
 return maxi and all(h.bit_count()==3 for h in maxi)
random.seed(42)
assert kd(start,1) and not kd(start,0)
t=time.time()
for trial in range(30):
 fs=start
 while True:
  candidates=[f for f in allfs if f not in fs and shelladd(fs,f)];random.shuffle(candidates)
  vdexists=False
  for f in candidates:
   nf=tuple(sorted(fs+(f,)))
   if kd(nf,0):vdexists=True;continue
   if kd(nf,1):
    fs=nf
    print('step',trial,len(fs),'time',time.time()-t,'cache',kd.cache_info(),flush=True)
    break
  else:
   print('terminal',trial,len(fs),'VDescape',vdexists,'time',time.time()-t,'cache',kd.cache_info(),flush=True)
   if not vdexists:
    print('STUCK',fs);pickle.dump(fs,open('workspace/agent4_edge_stuck.pkl','wb'))
   break
 if kd.cache_info().currsize>500000:kd.cache_clear()

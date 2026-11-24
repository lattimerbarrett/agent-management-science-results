import sys,itertools,json,time
sys.path.insert(0,'workspace')
from agent2_completion_light import complete_light

def ideals(n):
 if n==0:return [0,1]
 prev=ideals(n-1); shift=1<<(n-1)
 return [a|(b<<shift) for a in prev for b in prev if b&a==b]

def bier(K,n):
 facets=[]
 for f in range(1<<n):
  if not K>>f&1:continue
  for i in range(n):
   if f>>i&1 or K>>(f|1<<i)&1:continue
   facets.append(tuple(j for j in range(n) if f>>j&1)+tuple(n+j for j in range(n) if not (f|1<<i)>>j&1))
 verts=sorted(set(v for f in facets for v in f));mp={v:i for i,v in enumerate(verts)}
 return [tuple(mp[v] for v in f) for f in facets],len(verts)

def verify(fs,n,order):
 old={0}; seen=set()
 def add(f):
  for r in range(5):
   for h in itertools.combinations(f,r):old.add(sum(1<<x for x in h))
 for f in fs:add(f);seen.add(sum(1<<x for x in f))
 for f in order:
  assert f not in seen;seen.add(f)
  vv=[x for x in range(n) if f>>x&1]
  rr=[f^(1<<v) for v in vv if (f^(1<<v)) in old]
  assert rr
  for r in range(4):
   for h in itertools.combinations(vv,r):
    g=sum(1<<v for v in h)
    assert g not in old or any(g&ridge==g for ridge in rr)
  add(vv)
 assert all(sum(1<<v for v in h) in old for h in itertools.combinations(range(n),3))

ids=ideals(5);assert len(ids)==7581 and len(set(ids))==7581
count=0; byn={}; start=time.time()
for K in ids:
 if K in (0,(1<<32)-1):continue
 fs,n=bier(K,5)
 assert fs and all(len(f)==4 for f in fs)
 ans=complete_light(fs,n,seed=0)
 if not ans[0]:
  print('TRAP',K,fs,n,flush=True);json.dump({'K':K,'facets':fs,'n':n,'addition':ans[3]},open('workspace/agent3_bier_trap.json','w'));break
 verify(fs,n,ans[3])
 count+=1;byn[n]=byn.get(n,0)+1
 if count%1000==0:print(count,time.time()-start,flush=True)
else:print('ALL COMPLETE',count,byn,time.time()-start,flush=True)

import itertools,random,time,json,sys
sys.path.insert(0,'workspace')
from agent4_checker import dec

def rank2(rows):
 piv={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in piv:x^=piv[p]
   else:piv[p]=x;break
 return len(piv)

def search(n,trials):
 edges=[sum(1<<v for v in c) for c in itertools.combinations(range(n),2)];eidx={e:i for i,e in enumerate(edges)}
 tris=[sum(1<<v for v in c) for c in itertools.combinations(range(n),3)];tidx={t:i for i,t in enumerate(tris)}
 tedges={t:[e for e in edges if e&t==e] for t in tris}
 tb={t:sum(1<<eidx[e] for e in tedges[t]) for t in tris}
 fs=[sum(1<<v for v in c) for c in itertools.combinations(range(n),4)]
 ft={f:{t for t in tris if t&f==t} for f in fs}
 partial=0;h1zero=0;start=time.time()
 for trial in range(trials):
  random.shuffle(fs);T=set()
  for f in fs:
   T.update(ft[f])
   change=True
   while change:
    change=False
    for g in fs:
     if len(ft[g]&T)==3:
      T.update(ft[g]);change=True
   if len(T)==len(tris):break
   if set.union(*(set(tedges[t]) for t in T))!=set(edges):continue
   partial+=1
   h1=len(edges)-n+1-rank2([tb[t] for t in T])
   if h1==0:
    h1zero+=1;facets=tuple(sorted(g for g in fs if ft[g]<=T))
    print('H1zero terminal',n,'trial',trial,'facets',len(facets),'triangles',len(T),facets,flush=True)
    json.dump({'n':n,'facets':facets},open('workspace/agent4_terminal_h1zero.json','w'))
    print('dec3?',dec(facets,3),flush=True);return
  if trial%1000==0:print('trial',n,trial,'partial',partial,'h1zero',h1zero,'time',time.time()-start,flush=True)
 print('none',n,trials,partial,flush=True)
random.seed(1245)
search(9,10000)
search(10,10000)

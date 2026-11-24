import networkx as nx,itertools,random,pickle,time
import numpy as np
from scipy.special import iv
rng=random.Random(2026);x=float(iv(2,2)/iv(1,2))
def requirements(H,aa,k):
 pairs=list(itertools.combinations(range(k),2)); idx={p:i for i,p in enumerate(pairs)};reqs=set();matching=False;critical=False
 n=len(H);E=list(H.edges())
 for mask in range(1<<(n-1)):
  col=[(mask>>i)&1 for i in range(n)]
  same=[(u,v) for u,v in E if col[u]==col[v]]
  if len(same)==1:critical=True;break
  R=set(v for e in same for v in e)
  if len(R)==2*len(same) and (all(col[v]==0 for v in R) or all(col[v]==1 for v in R)):matching=True
  for flip in [0,1]:
   RA=[v for v in R if col[v]==flip];RB=[v for v in R if col[v]!=flip]
   if len(RA)>aa or len(RB)>k-aa:continue
   ER=[(u,v) for u,v in E if u in R and v in R]
   for pa in itertools.permutations(range(aa),len(RA)):
    for pb in itertools.permutations(range(aa,k),len(RB)):
     mp=dict(zip(RA+RB,pa+pb));req=0
     for u,v in ER:
      p,q=sorted((mp[u],mp[v]));req|=1<<idx[p,q]
     reqs.add(req)
 if critical or not matching:return None
 minimal=[]
 for req in sorted(reqs,key=int.bit_count):
  if not any(req&v==v for v in minimal):minimal.append(req)
 return tuple(sorted(minimal))
def host_arrays(k,aa):
 pairs=list(itertools.combinations(range(k),2));masks=np.arange(1<<len(pairs),dtype=np.int64)
 ea=np.zeros(len(masks),dtype=np.int8);eb=ea.copy();miss=ea.copy()
 for bit,(i,j) in enumerate(pairs):
  bitvals=((masks>>bit)&1).astype(np.int8)
  if j<aa:ea+=bitvals
  elif i>=aa:eb+=bitvals
  else:miss+=1-bitvals
 return masks,ea+eb-miss,np.maximum((1+x)*ea+x*eb,(1+x)*eb+x*ea)-miss,ea,eb,miss
k=7;aa=3;arrays=host_arrays(k,aa);masks,edges,weight,ea,eb,miss=arrays
seen=set();count=0;start=time.time()
for trial in range(3000):
 n=rng.randrange(8,13);T=nx.from_prufer_sequence([rng.randrange(n-1) for _ in range(n-3)])
 H=T.copy();H.add_node(n-1)
 H.add_edges_from((v,n-1) for v in range(n-1) if rng.random()<.6)
 if nx.is_bipartite(H):continue
 reqs=requirements(H,aa,k)
 if reqs is None or reqs in seen:continue
 seen.add(reqs);count+=1
 good=np.ones(len(masks),dtype=bool)
 for req in reqs:good&=(masks&req)!=req
 if not good.any():continue
 me=edges[good].max();mw=weight[good].max();ew=weight[good&(edges==me)].max()
 if mw>ew+1e-7:
  print('FOUND',list(H.edges()),'me',me,'ew',ew,'mw',mw,flush=True)
  ids=np.where(good&((weight>mw-1e-7)|((edges==me)&(weight>ew-1e-7))))[0]
  for i in ids[:20]:print(' mask',int(masks[i]),'e,w',int(edges[i]),float(weight[i]),'ea,eb,miss',ea[i],eb[i],miss[i])
  with open('bounded_candidate.pkl','wb') as f:pickle.dump((H,k,aa,reqs,arrays),f)
  break
 if trial%100==0:print('trial',trial,'distinct',count,'elapsed',time.time()-start,flush=True)
else:print('none; distinct',count)
